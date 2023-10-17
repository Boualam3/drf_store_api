import pytest
from rest_framework import status
from model_bakery import baker
from store.models import Product, Collection

# keep that in mind we test the behavior not the implementation ,
# the implementation change but the behavior does not .
# the name of function should be start with test_"the behavior we want to test"
# the name of class should be start with Test or pytest not recognize the test

# * the idea is to simplify and follow the DRY rule by dont call APIclient each time we use fixture decorator that help us to pass it as parameter on test function then access it


# * also we want to make this line reusable "api_client.post('/store/collections/', data)" like we did in api_client fixture but this time we want to return function that take dynamic data for pass it  , we do that because we cant pass another parameter to function that decorate by fixture , pytest will think it is fixture and will try to find it

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:

    def test_if_user_is_anonymous_return_401(self,  create_collection):

        # api_client it is fixture define in conftest
        response = create_collection({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_not_admin_returns_403(self,  create_collection, user_authenticate):
        user_authenticate()
        response = create_collection({'title': 'a'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self,  create_collection, user_authenticate):

        user_authenticate(is_staff=True)

        response = create_collection({'title': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self,  create_collection, user_authenticate):
        user_authenticate(is_staff=True)
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_return_200(self, api_client):
        # with baker we dont need to init each field on the model ,baker take care of that for us
        collection = baker.make(Collection)
        response = api_client.get(f"/store/collections/{collection.id}/")
        assert response.status_code == status.HTTP_200_OK


# this is eg how to use backer with Product
# collection = baker.make(Collection)
# baker.make(Product, collection=collection, _quantity=10)
