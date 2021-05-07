from sqlalchemy.orm import Session

from app import crud
from app.config import settings
from app.database.core import engine
from app.models import user
from app.schemas.user import UserCreateRequest


def user_seeder(db: Session):
    user.Base.metadata.create_all(bind=engine)

    one = UserCreateRequest(
        full_name="Chosen One",
        email="one@user.com",
        username=settings.ADMIN_USERNAME,
        password=settings.ADMIN_PASSWORD,
        admin=True,
    )
    two = UserCreateRequest(
        full_name="Morpheus",
        email="morpheus@user.com",
        username="morpheus",
        password=settings.ADMIN_PASSWORD,
        admin=False,
    )
    three = UserCreateRequest(
        full_name="Tank",
        email="tank@user.com",
        username="operator",
        password=settings.ADMIN_PASSWORD,
        admin=False,
    )
    one_in_db = crud.get_user_by_username(db, username=one.username)
    two_in_db = crud.get_user_by_username(db, username=two.username)
    three_in_db = crud.get_user_by_username(db, username=three.username)
    if not one_in_db:
        crud.create_user(db, one)
    if not two_in_db:
        crud.create_user(db, two)
    if not three_in_db:
        crud.create_user(db, three)
