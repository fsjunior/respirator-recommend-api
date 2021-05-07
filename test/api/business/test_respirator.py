import pytest
from bs4 import BeautifulSoup

from app.api.business.respirator import RespiratorExtractor
from app.api.exceptions.respirator import ErrorParsingWebsite
from app.model.respirator import ApprovalCertificate, Respirator


class TestRespiratorExtractor:
    @classmethod
    def setup_class(cls):
        ApprovalCertificate.drop_collection()
        Respirator.drop_collection()

    @pytest.fixture()
    def approval_certificate(self):
        approval_certificate = ApprovalCertificate(number=666, manufacturer="test", good_ac=True)
        return approval_certificate.save()

    @pytest.fixture()
    def invalid_approval_certificate(self):
        approval_certificate = ApprovalCertificate(number=777, manufacturer="test", good_ac=False)
        return approval_certificate.save()

    def check_respirator(self, mocker, data_dict, mocked_file):
        mocker.patch(
            "app.api.business.respirator.RespiratorExtractor.fetch_website",
            lambda x, y: BeautifulSoup(mocked_file, "html.parser"),
        )

        respirator = RespiratorExtractor(url=data_dict["url"]).analyze_website()

        assert respirator.url == data_dict["url"], data_dict["url"]

        assert respirator.spandex == data_dict["spandex"]
        assert respirator.respirator_type == data_dict["respirator_type"]
        assert respirator.exhalation_valve == data_dict["exhalation_valve"]
        if data_dict["approval_certificate"] is not None:
            assert respirator.approval_certificate.number == data_dict["approval_certificate"]

    def test_pff2_in_title_analysis(self, mocker, approval_certificate):
        data_dict = {
            "approval_certificate": 666,
            "exhalation_valve": False,
            "respirator_type": "PFF2",
            "spandex": None,
            "url": "dummy",
        }

        mocked_file = """
            <!DOCTYPE HTML> 
            <html lang="pt-BR"> 
                <head> 	 
                    <title>Máscara test PFF2 S/V CA 666</title>
                </head>
            <body></body>
            </html>
        """

        self.check_respirator(mocker, data_dict, mocked_file)

    def test_pff2_in_body_analysis(self, mocker, approval_certificate):
        data_dict = {
            "approval_certificate": 666,
            "exhalation_valve": False,
            "respirator_type": "PFF2",
            "spandex": None,
            "url": "dummy",
        }

        mocked_file = """
            <!DOCTYPE HTML> 
            <html lang="pt-BR"> 
                <head> 	 
                    <title>Máscara test</title>
                </head>
            <body>
            <h1>Máscara test PFF2 S/V</h1>
            <div>CA 666</div>
            </body>
            </html>
        """

        self.check_respirator(mocker, data_dict, mocked_file)

    def test_pff2_without_valid_ac(self, mocker, invalid_approval_certificate):
        mocked_file = """
            <!DOCTYPE HTML> 
            <html lang="pt-BR"> 
            <title>Máscara test PFF2 S/V CA 777</title>
            <body></body>
            </html>
        """

        mocker.patch(
            "app.api.business.respirator.RespiratorExtractor.fetch_website",
            lambda x, y: BeautifulSoup(mocked_file, "html.parser"),
        )

        respirator = RespiratorExtractor(url="dummy").analyze_website()

        assert respirator.approval_certificate is None

    def test_extract_invalid_certificate(self):
        respirator_extractor = RespiratorExtractor(url="dummy")
        assert respirator_extractor._extract_approval_certificate(ac_candidate="asdasd", title="") is False

    def test_spandex_analysis(self, mocker):
        data_dict = {
            "approval_certificate": None,
            "exhalation_valve": None,
            "respirator_type": None,
            "spandex": True,
            "url": "dummy",
        }

        mocked_file = """
            <!DOCTYPE HTML> 
            <html lang="pt-BR"> 
                <head> 	 
                    <title>Máscara da Cueca com elastano</title>
                </head>
            <body><div>Mascara com 100% elastano.</div></body>
            </html>
        """

        self.check_respirator(mocker, data_dict, mocked_file)

    def test_should_raise_error_parsing_website(self, mocker):
        mocker.patch("app.api.business.respirator.RespiratorExtractor.fetch_website", return_value=None)

        with pytest.raises(ErrorParsingWebsite):
            RespiratorExtractor(url="dummy").analyze_website()
