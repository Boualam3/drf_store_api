import pytest
from rest_framework import status
from model_bakery import baker
from store.models import Product, Collection


@pytest.fixture
def create_product(api_client):
    collection = baker.make(Collection)
    product = baker.make(Product, collection=collection, _quantity=10)
    return api_client.post(f'/store/products/', product)


@pytest.mark.skip(reason="Skipping the entire class due to incomplete implementation")
@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_return_401(self, create_product):

        # api_client it is fixture define in conftest
        response = create_product()
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_not_admin_returns_403(self,  user_authenticate, create_product):
        user_authenticate()
        response = create_product()
        assert response.status_code == status.HTTP_403_FORBIDDEN
