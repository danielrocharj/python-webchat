def test_users_get_returns_status_200(client_app):
    response = client_app.get("/users")
    assert response.status_code == 200


def test_users_get_returns_users_list(client_app):
    response = client_app.get("/users")
    assert response.json() == [{"username": "user1"}, {"username": "user2"}]


def test_users_me_returns_status_200(client_app):
    response = client_app.get("/users/me")
    assert response.status_code == 200


def test_users_me_returns_user(client_app):
    response = client_app.get("/users/me")
    assert response.json() == {"username": "user1"}


def test_users_user_returns_status_200(client_app):
    response = client_app.get("/users/user")
    assert response.status_code == 200


def test_users_user_returns_user(client_app):
    response = client_app.get("/users/user")
    assert response.json() == {"username": "user"}
