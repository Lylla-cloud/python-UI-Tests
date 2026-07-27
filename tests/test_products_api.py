import pytest
import requests
from utils.config_reader import ConfigReader


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(scope="session")
def base_url():
    return ConfigReader.get("api_base_url")


class TestProductsApi:

    def test_get_all_products_returns_array(self, api_session, base_url):
        response = api_session.get(f"{base_url}/productsList")
        assert response.status_code == 200
        body = response.json()
        assert body.get("responseCode") == 200
        assert "products" in body
        assert isinstance(body["products"], list)

    def test_get_all_products_not_empty(self, api_session, base_url):
        response = api_session.get(f"{base_url}/productsList")
        assert response.status_code == 200
        body = response.json()
        assert body.get("responseCode") == 200
        assert len(body["products"]) > 0

    def test_product_data_structure(self, api_session, base_url):
        response = api_session.get(f"{base_url}/productsList")
        assert response.status_code == 200
        body = response.json()
        assert body.get("responseCode") == 200
        first_product = body["products"][0]
        assert "id" in first_product
        assert "name" in first_product
        assert "price" in first_product
        assert "category" in first_product

    def test_get_all_brands_returns_array(self, api_session, base_url):
        response = api_session.get(f"{base_url}/brandsList")
        assert response.status_code == 200
        body = response.json()
        assert body.get("responseCode") == 200
        assert "brands" in body
        assert len(body["brands"]) > 0

    def test_search_product_happy_path(self, api_session, base_url):
        response = api_session.post(
            f"{base_url}/searchProduct",
            data={"search_product": "dress"}
        )
        assert response.status_code == 200
        body = response.json()
        assert body.get("responseCode") == 200
        assert len(body["products"]) > 0

    def test_search_product_missing_parameter(self, api_session, base_url):
        response = api_session.post(f"{base_url}/searchProduct")
        assert response.status_code == 200
        body = response.json()
        assert body.get("responseCode") == 400
        assert "parameter is missing" in body.get("message", "")

    def test_invalid_method_on_products(self, api_session, base_url):
        response = api_session.delete(f"{base_url}/productsList")
        assert response.status_code == 200
        body = response.json()
        assert body.get("responseCode") == 405
        assert "not supported" in body.get("message", "").lower()

    def test_response_time_acceptable(self, api_session, base_url):
        response = api_session.get(f"{base_url}/productsList")
        assert response.status_code == 200
        assert response.elapsed.total_seconds() < 5.0, \
            f"Response too slow: {response.elapsed.total_seconds():.2f}s"


class TestUserApi:

    def test_verify_login_success(self, api_session, base_url):
        response = api_session.post(
            f"{base_url}/verifyLogin",
            data={
                "email": ConfigReader.get_nested("test_user", "email"),
                "password": ConfigReader.get_nested("test_user", "password")
            }
        )
        assert response.status_code == 200
        body = response.json()
        assert body.get("responseCode") == 200
        assert "User exists" in body.get("message", "")

    def test_verify_login_wrong_credentials(self, api_session, base_url):
        response = api_session.post(
            f"{base_url}/verifyLogin",
            data={"email": "wrong@test.com", "password": "wrongpass"}
        )
        assert response.status_code == 200
        body = response.json()
        assert body.get("responseCode") == 404
        assert "User not found" in body.get("message", "")

    def test_verify_login_missing_email(self, api_session, base_url):
        response = api_session.post(
            f"{base_url}/verifyLogin",
            data={"password": "password123"}
        )
        assert response.status_code == 200
        body = response.json()
        assert body.get("responseCode") == 400
        assert "parameter is missing" in body.get("message", "")

    def test_verify_login_invalid_method(self, api_session, base_url):
        response = api_session.get(f"{base_url}/verifyLogin")
        assert response.status_code == 200
        body = response.json()
        assert body.get("responseCode") == 405
        assert "not supported" in body.get("message", "").lower()