import pytest
from fastapi.testclient import TestClient
from sqlalchemy_utils import drop_database
from app.config import settings

settings.ENVIRONMENT = "test"

from app.database import SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import user  # noqa: E402


@pytest.fixture(scope="session")
def db():
    user.Base.metadata.create_all(bind=engine)
    yield SessionLocal()
    drop_database(engine.url)


@pytest.fixture(scope="module")
def client_app():
    with TestClient(app) as Client:
        yield Client
