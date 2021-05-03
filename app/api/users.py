from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from app import dependencies, crud
from app.schemas.user import User, UserCreateRequest
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[User])
async def list_all_users(
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    db: Session = Depends(dependencies.get_db),
):
    """Return all users"""
    users = crud.get_users(db, skip, limit)
    return users


@router.post("/", response_model=User, status_code=201)
async def create_user(
    user_request: UserCreateRequest, db: Session = Depends(dependencies.get_db)
):
    """Create a new user"""
    user_by_email = crud.get_user_by_email(db, user_request.email)
    user_by_username = crud.get_user_by_username(db, user_request.username)
    if user_by_email or user_by_username:
        raise HTTPException(status_code=400, detail="The user already exists.")
    return crud.create_user(db, user_request)


# @router.get("/me")
# async def list_user_me():
#     """Grab information about the logged user"""
#     return {"username": "user1"}


@router.get("/{username}", response_model=User)
async def list_user_by_username(
    username: str, db: Session = Depends(dependencies.get_db)
):
    """Grab information about user by username"""
    return crud.get_user_by_username(db, username)
