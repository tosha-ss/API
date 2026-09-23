import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from catalog.models import Category


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(username="test_user", password="password123"):
        return User.objects.create_user(username=username, password=password)

    return make_user

@pytest.fixture
def auth_client(db, api_client, create_user):
    user = create_user(username="tosha")

    from rest_framework_simplejwt.tokens import RefreshToken
    access_token = str(RefreshToken.for_user(user).access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    api_client.user = user
    return api_client


@pytest.fixture
def test_category(db):
    return Category.objects.create(name="Тестовая Категория", slug="test-cat")
