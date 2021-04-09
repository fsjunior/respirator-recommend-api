from bs4 import BeautifulSoup
import locale
from typing import List, Type
import requests
from fake_headers import Headers


from app.api.business.common import find_by_id
from app.api.exceptions.respirator import RespiratorNotFound, CannotOpenWebsite, CannotCheckACWebsite, \
    ErrorParsingACWebsite, MalformedURL, ErrorParsingWebsite
from app.model.respirator import Respirator, ApprovalCertificate
from app.nlp import nlp


def find_respirator_by_id(doc_class: Type[Respirator], doc_id: str) -> Respirator:
    return find_by_id(doc_class, doc_id, RespiratorNotFound)


def _find_first(values: List[str], dictionary: dict):
    for value in values:
        if value in dictionary:
            return value
    return None


class ApprovalCertificateExtractor:
    def __init__(self, number: int):
        self.approval_certificate = ApprovalCertificate.objects(number=number).first()

        if self.approval_certificate is None:
            self.approval_certificate = ApprovalCertificate(number=number, good_ac=False)
            soup = self._download_website()
            self.parse_website(soup)
            self.approval_certificate.save()

    def _download_website(self) -> BeautifulSoup:
        headers = Headers(headers=True).generate()
        res = requests.get(f'https://consultaca.com/{self.approval_certificate.number}', timeout=1.0, headers=headers)
        if res.status_code != 200:
            raise CannotCheckACWebsite()
        return BeautifulSoup(res.text, 'html.parser')

    def parse_website(self, soup: BeautifulSoup):
        title = soup.find_all('title')[0].get_text().lower()
        text = nlp(title)

        detected_labels = {entity.label_: entity.text for entity in text.ents}

        ac_class = _find_first(["PFF3", "PFF2", "PFF1"], detected_labels)
        if ac_class is None:
            return

        self.approval_certificate.ac_class = ac_class

        try:
            self.approval_certificate.valid = soup.find('div', {'id': 'box_result'}).find_all('p')[7].span.get_text().lower() == 'válido'
        except IndexError as ie:
            raise ErrorParsingACWebsite() from ie

        try:
            self.approval_certificate.manufacturer = title.split(' - ')[-1].split(' ')[0].lower()
        except IndexError as ie:
            raise ErrorParsingACWebsite() from ie

        self.approval_certificate.good_ac = True


class RespiratorExtractor:
    def __init__(self, url: str):
        self.respirator = Respirator(url=url)
        self.url = url

    def _download_website(self) -> BeautifulSoup:
        headers = Headers(headers=True).generate()
        try:
            res = requests.get(self.url, timeout=1.0, headers=headers)
        except requests.exceptions.MissingSchema as ms:
            raise MalformedURL() from ms
        except requests.exceptions.RequestException as re:
            raise CannotOpenWebsite from re

        if res.status_code != 200:
            raise CannotOpenWebsite

        try:
            return BeautifulSoup(res.text, 'html.parser')
        except Exception as ex:
            raise CannotOpenWebsite from ex

    def analyze_title(self, title: str):
        text = nlp(title)

        detected_labels = {entity.label_: entity.text for entity in text.ents}

        respirator_type = _find_first(["KN95", "PFF3", "PFF2", "PFF1"], detected_labels)
        if respirator_type is not None:
            self.respirator.respirator_type = respirator_type

        exhalation_valve = _find_first(["CV", "SV"], detected_labels)
        if exhalation_valve is not None:
            self.respirator.exhalation_valve = exhalation_valve == "CV"

        if "EL" in detected_labels:
            self.respirator.spandex = True

        if "QT" in detected_labels:
            try:
                self.respirator.quantity = locale.atoi(detected_labels["QT"])
            except ValueError:
                self.respirator.quantity = 1
        else:
            self.respirator.quantity = 1

        if "CA" in detected_labels:
            self._extract_ac(detected_labels["CA"], title)

    def _extract_ac(self, ac_candidate, title):
        try:
            number = locale.atoi(ac_candidate)
        except ValueError:
            return False

        ac = ApprovalCertificateExtractor(number).approval_certificate

        if ac.good_ac and ac.manufacturer in title:
            self.respirator.approval_certificate = ac
            return True

        return False

    def search_ac(self, body: str, title: str):
        text = nlp(body)

        for entity in text.ents:
            if "CA" in entity.label_:
                if self._extract_ac(entity.text, title):
                    break

    def search_el(self, body: str):
        text = nlp(body)

        for entity in text.ents:
            if "EL" in entity.label_:
                self.respirator.spandex = True

    def analyze_website(self) -> Respirator:
        soup = self._download_website()
        try:
            title = soup.title.get_text().lower()
            body = soup.body.get_text().lower()
        except (IndexError, AttributeError) as ex:
            raise ErrorParsingWebsite from ex

        self.analyze_title(title)

        if self.respirator.respirator_type:
            if self.respirator.respirator_type == "PFF2" and not self.respirator.approval_certificate:
                self.search_ac(body, title)
        else:
            self.search_el(body)
        return self.respirator


