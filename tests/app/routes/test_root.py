def test_root_returns_status_200(client_app):
    response = client_app.get("/")
    assert response.status_code == 200


def test_root_returns_msg(client_app):
    response = client_app.get("/")
    assert response.json() == {"msg": "Python Webchat"}


def test_ping_returns_status_200(client_app):
    response = client_app.get("/echo")
    assert response.status_code == 200


def test_ping_returns_pong(client_app):
    response = client_app.get("/echo")
    assert response.text == "echo! echo! echo!"
