import pytest



@pytest.mark.django_db
def test_full_auth_scenario(api_client, create_user):

    create_user(username="misha", password="secret_password_123")


    login_data = {"username": "misha", "password": "secret_password_123"}
    token_response = api_client.post('/api/token/', login_data)
    assert token_response.status_code == 200
    access_token = token_response.data["access"]

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    me_response = api_client.get('/api/me/')

    assert me_response.status_code == 200
    assert me_response.data["username"] == "misha"


@pytest.mark.django_db
def test_me_endpoint_without_token_returns_401(api_client):
    response = api_client.get('/api/me/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_wrong_password_returns_401(api_client, create_user):
    create_user(username="misha", password="correct_password")
    wrong_data = {"username": "misha", "password": "WRONG_password"}
    response = api_client.post('/api/token/', wrong_data)
    assert response.status_code == 401
