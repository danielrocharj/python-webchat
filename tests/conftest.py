import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy_utils import drop_database

from app.config import settings
from app.security import create_jwt_token

settings.ENVIRONMENT = "TEST"

from app.database.core import SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import user  # noqa: E402
from app.schemas.user import UserCreateRequest  # noqa: E402
from app import crud  # noqa: E402

faker = Faker()


@pytest.fixture(scope="session")
def db():
    user.Base.metadata.create_all(bind=engine)
    admin_user = UserCreateRequest(
        full_name="Chosen One",
        email="one@user.com",
        username=settings.ADMIN_USERNAME,
        password=settings.ADMIN_PASSWORD,
        admin=True,
    )
    crud.create_user(SessionLocal(), admin_user)
    yield SessionLocal()
    drop_database(engine.url)


@pytest.fixture(scope="module")
def client_app():
    with TestClient(app) as Client:
        yield Client


@pytest.fixture(scope="module")
def admin_token_header(db: SessionLocal()):
    admin_token = create_jwt_token(settings.ADMIN_USERNAME)
    headers = {"Authorization": f"Bearer {admin_token}"}
    return headers


@pytest.fixture(scope="module")
def user_token_header(db: SessionLocal()):
    user = UserCreateRequest(
        full_name=faker.name(),
        email=faker.email(),
        username=faker.word(),
        password=faker.md5(),
        admin=False,
    )

    if not crud.get_user_by_username(db, username=user.username):
        crud.create_user(db, user)

    user_token = create_jwt_token(user.username)
    headers = {"Authorization": f"Bearer {user_token}"}
    return headers
