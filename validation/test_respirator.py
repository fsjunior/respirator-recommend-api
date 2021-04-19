import json
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from app.api.business.respirator import RespiratorExtractor
from app.model.respirator import ApprovalCertificate, Respirator


def mocked_extract_approval_certificate(self: RespiratorExtractor, ac_real: int, ac_candidate: str, _: str = None):
    try:
        number = int(ac_candidate.replace(".", ""))
    except (ValueError, AttributeError):
        return False

    if ac_real == number:
        self.respirator.approval_certificate = ApprovalCertificate(number=number, good_ac=True)
        return True

    return False


class TestRespirator:
    DATA_PATH = Path("validation/data/")

    @classmethod
    def setup_class(cls):
        ApprovalCertificate.drop_collection()
        Respirator.drop_collection()

    def test(self, mocker):
        for file in self.DATA_PATH.glob("*.json"):
            with file.open("r") as f:
                data_dict = json.load(f)
                respirator_args = dict(url=data_dict["url"])

                mocker.patch(
                    "app.api.business.respirator.RespiratorExtractor.fetch_website",
                    lambda x, y: BeautifulSoup(open(self.DATA_PATH / data_dict["data_file"]).read(), "html.parser"),
                )

                mocker.patch(
                    "app.api.business.respirator.RespiratorExtractor._extract_approval_certificate",
                    lambda x, ac, title: mocked_extract_approval_certificate(
                        x, data_dict["approval_certificate"], ac, title
                    ),
                )

                respirator = RespiratorExtractor(**respirator_args).analyze_website()

                assert respirator.url == data_dict["url"], data_dict["url"]

                assert respirator.spandex == data_dict["spandex"], data_dict["url"]
                assert respirator.respirator_type == data_dict["respirator_type"], data_dict["url"]
                # assert respirator.quantity == data_dict["quantity"], data_dict["url"]
                assert respirator.exhalation_valve == data_dict["exhalation_valve"], data_dict["url"]
                if data_dict["approval_certificate"]:
                    assert respirator.approval_certificate.number == data_dict["approval_certificate"], data_dict["url"]
