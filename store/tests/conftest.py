import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

# now this function is reusable piece of code we can add it to each test as parameter


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_authenticate(api_client):
    def do_authenticate_user(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate_user
