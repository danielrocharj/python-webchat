from sqlalchemy.orm import Session
from faker import Faker
from app import crud
from app.schemas.user import UserCreateRequest


faker = Faker()


def test_create_user(db: Session):
    profile1 = faker.simple_profile()
    user_request = UserCreateRequest(
        full_name=profile1["name"],
        username=profile1["username"],
        email=profile1["mail"],
        password=faker.md5(),
    )
    user = crud.create_user(db, user_request)
    assert user
    assert user.username == user_request.username


def test_get_user_by_id(db: Session):
    profile2 = faker.simple_profile()
    user_request = UserCreateRequest(
        full_name=profile2["name"],
        username=profile2["username"],
        email=profile2["mail"],
        password=faker.md5(),
    )
    user_in_db = crud.create_user(db, user_request)
    result = crud.get_user_by_id(db, user_in_db.id)
    assert result
    assert user_in_db.id == result.id


def test_get_user_by_username(db: Session):
    profile3 = faker.simple_profile()
    user_request = UserCreateRequest(
        full_name=profile3["name"],
        username=profile3["username"],
        email=profile3["mail"],
        password=faker.md5(),
    )
    user_in_db = crud.create_user(db, user_request)
    result = crud.get_user_by_username(db, user_in_db.username)
    assert result
    assert user_request.username == result.username


def test_get_user_by_email(db: Session):
    profile3 = faker.simple_profile()
    user_request = UserCreateRequest(
        full_name=profile3["name"],
        username=profile3["username"],
        email=profile3["mail"],
        password=faker.md5(),
    )
    user_in_db = crud.create_user(db, user_request)
    result = crud.get_user_by_email(db, user_in_db.email)
    assert result
    assert user_request.email == result.email
