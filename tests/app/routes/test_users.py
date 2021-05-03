from faker import Faker

faker = Faker()


def test_users_get_returns_status_200(client_app):
    response = client_app.get("/users")
    assert response.status_code == 200


def test_users_get_returns_users_list(client_app):
    query_params = {"skip": 0, "limit": 10}
    response = client_app.get("/users", params=query_params)
    result = response.json()
    assert len(result) <= 10


# def test_users_me_returns_status_200(client_app):
#     response = client_app.get("/users/me")
#     assert response.status_code == 200
#
#
# def test_users_me_returns_user(client_app):
#     response = client_app.get("/users/me")
#     assert response.json() == {"username": "user1"}


def test_list_user_returns_status_200(client_app):
    response = client_app.get("/users/user")
    assert response.status_code == 200


def test_list_user_returns_user(client_app):
    user_request = {
        "full_name": faker.name(),
        "username": faker.word(),
        "email": faker.email(),
        "password": faker.md5(),
    }
    created_user = client_app.post("/users/", json=user_request)
    response = client_app.get("/users/" + user_request["username"])
    assert response.json() == created_user.json()


def test_create_user_returns_created_user(client_app):
    user_request = {
        "full_name": faker.name(),
        "username": faker.word(),
        "email": faker.email(),
        "password": faker.md5(),
    }
    result = client_app.post("/users/", json=user_request)
    created_user = result.json()
    assert result.status_code == 201
    assert user_request["email"] == created_user["email"]


def test_list_user_by_username_returns_200(client_app):
    username = faker.word()
    response = client_app.get("/users/" + username)
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
