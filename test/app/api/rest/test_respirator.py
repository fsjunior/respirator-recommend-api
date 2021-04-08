from http import HTTPStatus

import pytest

from app.model.respirator import Respirator


class TestRecipe:
    @classmethod
    def setup_class(cls):
        Respirator.drop_collection()

    # @pytest.fixture()
    # def new_respirator(self):
    #     return {"title": "ovo cozido", "ingredients": ["ovo", "água"], "howto": "cozinhe o ovo na água"}

    @pytest.fixture()
    def document_respirator(self):
        respirator = Respirator(quantity=1, url="https://www.pudim.com.br")
        return respirator.save()
    #
    # def test_should_post_recipe(self, client, new_respirator):
    #     response = client.post(
    #         "/api/v1/recipes",
    #         json=new_respirator,
    #     )
    #     assert response.status_code == HTTPStatus.CREATED
    #
    #     info_recipe = response.json
    #     assert info_recipe
    #     assert "id" in info_recipe
    #     assert info_recipe["id"] is not None
    #     assert "title" in info_recipe
    #     assert info_recipe["title"] == new_recipe["title"]
    #     assert info_recipe["howto"] is not None
    #     assert info_recipe["howto"] == new_recipe["howto"]
    #     assert info_recipe["ingredients"] is not None
    #     assert type(info_recipe["ingredients"]) is list
    #     assert sorted(info_recipe["ingredients"]) == sorted(new_recipe["ingredients"])
    #
    #     new_recipe_document = Respirator.objects(id=info_recipe["id"]).first()
    #     assert new_recipe_document is not None
    #
    #     assert new_recipe_document.title == new_recipe["title"]

    # def test_should_get_recipe_by_id(self, client, document_recipe):
    #     response = client.get(f"/api/v1/recipes/{document_recipe.id}")
    #     assert response.status_code == HTTPStatus.OK
    #
    #     info_recipe = response.json
    #     assert info_recipe
    #     assert "id" in info_recipe
    #     assert info_recipe["id"] is not None
    #     assert "title" in info_recipe
    #     assert info_recipe["title"] == document_recipe.title
    #     assert info_recipe["howto"] is not None
    #     assert info_recipe["howto"] == document_recipe.howto
    #     assert info_recipe["ingredients"] is not None
    #     assert type(info_recipe["ingredients"]) is list
    #     assert sorted(info_recipe["ingredients"]) == sorted(document_recipe.ingredients)
    #
    # def test_should_not_get_recipe_with_nonexistent_id(self, client):
    #     # fake id
    #     response = client.get("/api/v1/recipes/5f95ca454ff087dd3e3eae91")
    #     assert response.status_code == HTTPStatus.NOT_FOUND
    #
    # def test_should_not_get_recipe_with_wrong_id(self, client):
    #     # wrong id
    #     response = client.get("/api/v1/recipes/wrong_id")
    #     assert response.status_code == HTTPStatus.BAD_REQUEST
    #     response_json = response.json
    #
    #     assert "code" in response_json
    #     assert "message" in response_json
    #
    # def test_should_update_recipe_by_id(self, client, document_recipe):
    #     response = client.get(f"/api/v1/recipes/{document_recipe.id}")
    #     assert response.status_code == HTTPStatus.OK
    #
    #     recipe = response.json
    #
    #     del recipe["id"]
    #     recipe["ingredients"].append("sal")
    #     recipe["howto"] = "frite o ovo na frigideira. sal a gosto"
    #
    #     response = client.put(f"/api/v1/recipes/{document_recipe.id}", json=recipe)
    #
    #     assert response.status_code == HTTPStatus.OK
    #
    #     info_recipe = response.json
    #
    #     assert info_recipe
    #     assert "id" in info_recipe
    #     assert info_recipe["id"] is not None
    #     assert "title" in info_recipe
    #     assert info_recipe["title"] == recipe["title"]
    #     assert info_recipe["howto"] is not None
    #     assert info_recipe["howto"] == recipe["howto"]
    #     assert info_recipe["ingredients"] is not None
    #     assert type(info_recipe["ingredients"]) is list
    #     assert sorted(info_recipe["ingredients"]) == sorted(recipe["ingredients"])
    #
    # def test_should_delete_recipe_by_id(self, client, document_recipe):
    #     response = client.delete(f"/api/v1/recipes/{document_recipe.id}")
    #     assert response.status_code == HTTPStatus.NO_CONTENT
    #
    def test_should_get_all_recipes(self, client, document_respirator):
        response = client.post("/api/v1/respirator")
        assert response.status_code == HTTPStatus.OK

        info_respirator = response.json
        assert info_respirator
        assert type(info_respirator) is dict
        assert "id" in info_respirator
        assert "quantity" in info_respirator
        assert info_respirator["quantity"] == 1
