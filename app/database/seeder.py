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
        username="neo",
        email="one@user.com",
        password=settings.ADMIN_PASSWORD,
        admin=True,
    )
    user_in_db = crud.get_user_by_username(db, username=one.username)
    if not user_in_db:
        crud.create_user(db, one)
