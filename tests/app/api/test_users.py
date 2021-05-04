from faker import Faker
from app.config import settings

faker = Faker()


def test_users_get_returns_status_200(client_app, user_token_header):
    response = client_app.get("/users", headers=user_token_header)
    assert response.status_code == 200


def test_users_get_returns_users_list(client_app):
    query_params = {"skip": 0, "limit": 10}
    response = client_app.get("/users", params=query_params)
    result = response.json()
    assert len(result) <= 10


def test_users_me_returns_status_200(client_app, user_token_header):
    response = client_app.get("/users/me", headers=user_token_header)
    assert response.status_code == 200


def test_users_me_returns_user(client_app, admin_token_header):
    response = client_app.get("/users/me", headers=admin_token_header)
    result = response.json()
    assert result["username"] == settings.ADMIN_USERNAME


def test_list_user(client_app, admin_token_header):
    user_request = {
        "full_name": faker.name(),
        "username": faker.word(),
        "email": faker.email(),
        "password": faker.md5(),
    }
    created_user = client_app.post(
        "/users/", json=user_request, headers=admin_token_header
    )
    response = client_app.get(
        "/users/" + user_request["username"], headers=admin_token_header
    )
    assert response.status_code == 200
    assert response.json() == created_user.json()


def test_create_user_returns_created_user(client_app, admin_token_header):
    user_request = {
        "full_name": faker.name(),
        "username": faker.word(),
        "email": faker.email(),
        "password": faker.md5(),
    }
    result = client_app.post("/users/", json=user_request, headers=admin_token_header)
    created_user = result.json()
    assert result.status_code == 201
    assert user_request["email"] == created_user["email"]


def test_list_user_by_username_returns_200(client_app, admin_token_header):
    response = client_app.get(
        f"/users/{settings.ADMIN_USERNAME}", headers=admin_token_header
    )
    assert response.status_code == 200


def test_list_user_by_username_returns_user(client_app):
    user_request = {
        "full_name": faker.name(),
        "username": faker.word(),
        "email": faker.email(),
        "password": faker.md5(),
    }
    created_user = client_app.post("/users/", json=user_request)
    response = client_app.get("/users/" + user_request["username"])
    assert response.json() == created_user.json()
