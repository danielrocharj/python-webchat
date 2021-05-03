from typing import Any, Dict, Union
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreateRequest
from werkzeug.security import generate_password_hash


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_to_create: Union[UserCreateRequest, Dict[str, Any]]):
    db_user = User(
        full_name=user_to_create.full_name,
        username=user_to_create.username,
        email=user_to_create.email,
        password=generate_password_hash(user_to_create.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
