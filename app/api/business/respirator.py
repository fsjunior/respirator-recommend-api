from typing import List, Type

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from requests.adapters import HTTPAdapter

from app.api.business.common import find_by_id
from app.api.exceptions.respirator import CannotOpenWebsite, ErrorParsingWebsite, MalformedURL, RespiratorNotFound
from app.model.respirator import ApprovalCertificate, Respirator
from app.nlp import nlp


def find_respirator_by_id(doc_class: Type[Respirator], doc_id: str) -> Respirator:
    return find_by_id(doc_class, doc_id, RespiratorNotFound)


def _find_first(values: List[str], dictionary: dict):
    for value in values:
        if value in dictionary:
            return value
    return None


class BaseExtractor:
    @property
    def requests(self):
        session = requests.Session()
        session.mount("http://", HTTPAdapter(max_retries=3))
        session.mount("https://", HTTPAdapter(max_retries=3))
        return session

    def fetch_website(self, url):
        headers = Headers(headers=True).generate()
        try:
            res = self.requests.get(url, timeout=1.0, headers=headers)
        except requests.exceptions.MissingSchema as exception:
            raise MalformedURL() from exception
        except requests.exceptions.RequestException as exception:
            raise CannotOpenWebsite from exception

        if res.status_code != 200:
            raise CannotOpenWebsite

        try:
            return BeautifulSoup(res.text, "html.parser")
        except Exception as exception:
            raise ErrorParsingWebsite from exception


class ApprovalCertificateExtractor(BaseExtractor):
    def __init__(self, number: int):
        self.approval_certificate = ApprovalCertificate.objects(number=number).first()

        if self.approval_certificate is None:
            self.approval_certificate = ApprovalCertificate(number=number)
            soup = self.fetch_website(f"https://consultaca.com/{number}")
            self.parse_website(soup)
            self.approval_certificate.save()

    def parse_website(self, soup: BeautifulSoup):
        try:
            title = soup.title.get_text().lower()
        except (IndexError, AttributeError) as exception:
            raise ErrorParsingWebsite from exception

        text = nlp(title)

        detected_labels = {entity.label_: entity.text for entity in text.ents}

        ac_class = _find_first(["PFF3", "PFF2", "PFF1"], detected_labels)
        if ac_class is None:
            return

        self.approval_certificate.ac_class = ac_class

        try:
            self.approval_certificate.valid = (
                soup.find("div", {"id": "box_result"}).find_all("p")[7].span.get_text().lower() == "válido"
            )
            self.approval_certificate.manufacturer = title.split(" - ")[2].split(" ")[0].lower()
        except (IndexError, AttributeError) as exception:
            raise ErrorParsingWebsite from exception

        self.approval_certificate.good_ac = True


class RespiratorExtractor(BaseExtractor):
    def __init__(self, url: str):
        self.respirator = Respirator(url=url)
        self.url = url

    def analyze_title(self, title: BeautifulSoup):
        if self.respirator.title is None:
            self.respirator.title = title.get_text().strip()

        text = nlp(title.get_text().lower())

        detected_labels = {entity.label_: entity.text for entity in text.ents}

        respirator_type = _find_first(["KN95", "PFF3", "PFF2", "PFF1"], detected_labels)
        if respirator_type is not None and self.respirator.respirator_type is None:
            self.respirator.respirator_type = respirator_type

        exhalation_valve = _find_first(["CV", "SV"], detected_labels)
        if exhalation_valve is not None and self.respirator.exhalation_valve is None:
            self.respirator.exhalation_valve = exhalation_valve == "CV"

        if "EL" in detected_labels and self.respirator.spandex is None:
            self.respirator.spandex = True

        if self.respirator.quantity is None:
            if "QT" in detected_labels:
                try:
                    self.respirator.quantity = int(detected_labels["QT"].replace(".", ""))
                except (ValueError, AttributeError):
                    pass

        if "CA" in detected_labels and self.respirator.approval_certificate is None:
            self._extract_approval_certificate(detected_labels["CA"], None)

    def _extract_approval_certificate(self, ac_candidate: str, title: str = None):
        try:
            number = int(ac_candidate.replace(".", ""))
        except (ValueError, AttributeError):
            return False

        approval_certificate = ApprovalCertificateExtractor(number).approval_certificate

        if approval_certificate.good_ac:
            if title is None or approval_certificate.manufacturer in title:
                self.respirator.approval_certificate = approval_certificate
                return True

        return False

    def search_approval_certificate(self, body: BeautifulSoup, title: BeautifulSoup):
        for child in body.find_all(recursive=False):
            text = nlp(child.get_text().lower())
            for entity in text.ents:
                if "CA" in entity.label_:
                    if self._extract_approval_certificate(entity.text, title.get_text().lower()):
                        return

    def search_spandex(self, body: BeautifulSoup):
        for child in body.find_all(recursive=False):
            text = nlp(child.get_text().lower())
            for entity in text.ents:
                if "EL" in entity.label_:
                    self.respirator.spandex = True
                    return

    def analyze_website(self) -> Respirator:
        soup = self.fetch_website(self.respirator.url)
        try:
            title = soup.title
            body = soup.body
        except (IndexError, AttributeError) as ex:
            raise ErrorParsingWebsite from ex

        self.analyze_title(title)

        for tag_h1 in soup.find_all("h1")[:3]:
            self.analyze_title(tag_h1)

        if self.respirator.quantity is None:
            self.respirator.quantity = 1

        if self.respirator.respirator_type:
            if self.respirator.respirator_type == "PFF2" and not self.respirator.approval_certificate:
                self.search_approval_certificate(body, title)
        else:
            self.search_spandex(body)

        return self.respirator
