from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.dependencies import get_db
from app.schemas.user import User, UserCreateRequest
from sqlalchemy.orm import Session

from app.security import decode_jwt_token, oauth2_scheme

router = APIRouter()


def get_user_by_token(db: Session, token: str):
    payload = decode_jwt_token(token)
    user = crud.get_user_by_username(db, payload["username"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[User])
async def list_all_users(
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Return all users"""
    users = crud.get_users(db, skip, limit)
    return users


@router.post("/", response_model=User, status_code=201)
async def create_user(
    user_request: UserCreateRequest,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Create a new user"""
    user = get_user_by_token(db, token)
    if not user.admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    user_by_email = crud.get_user_by_email(db, user_request.email)
    user_by_username = crud.get_user_by_username(db, user_request.username)
    if user_by_email or user_by_username:
        raise HTTPException(status_code=400, detail="The user already exists.")
    return crud.create_user(db, user_request)


@router.get("/me", response_model=User)
async def list_user_me(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """Grab information about the logged user"""
    user = get_user_by_token(db, token)
    return user


@router.get("/{username}", response_model=User)
async def list_user_by_username(
    username: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """Grab information about user by username"""
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
