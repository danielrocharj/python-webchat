import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import ValidationError

from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_password(password_hash: str, password: str):
    return pwd_context.verify(password, password_hash)


def generate_hash(password: str):
    return pwd_context.hash(password)


def create_jwt_token(username: str):
    to_encode = {"username": username}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_jwt_token(token: str):
    try:
        return jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
    except ValidationError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
