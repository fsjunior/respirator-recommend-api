from http import HTTPStatus

import pytest
from bs4 import BeautifulSoup

from app.api.business.respirator import RespiratorExtractor
from app.model.respirator import Respirator


class TestRecipe:
    @classmethod
    def setup_class(cls):
        Respirator.drop_collection()

    def test_rest_api(self, client, mocker):
        mocked_file = """
                    <!DOCTYPE HTML> 
                    <html lang="pt-BR"> 
                        <head> 	 
                            <title>Máscara test PFF2 S/V CA 666</title>
                        </head>
                    <body></body>
                    </html>
                """

        mocker.patch(
            "app.api.business.respirator.RespiratorExtractor.fetch_website",
            lambda x, y: BeautifulSoup(mocked_file, "html.parser"),
        )

        response = client.post(f"/api/v1/respirator?url=https%3A%2F%2Fchico.codes")

        assert response.status_code == HTTPStatus.OK

        respirator = response.json

        assert respirator

        assert "url" in respirator
        assert respirator["url"] == "https://chico.codes"
        assert "title" in respirator
        assert respirator["title"] == "Máscara test PFF2 S/V CA 666"
