from app.security import validate_password, generate_hash


def test_generate_and_validate_password_returns_true():
    password = "password-plain1"
    password_hash = generate_hash(password)
    assert validate_password(password_hash, password)


def test_generate_and_validate_password_returns_false():
    password = "wordpass"
    password_hash = generate_hash("otherpass")
    assert not validate_password(password_hash, password)
