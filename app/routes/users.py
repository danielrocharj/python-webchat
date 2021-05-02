from fastapi import APIRouter

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    """Return all users"""
    return [{"username": "user1"}, {"username": "user2"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    """Grab information about the logged user"""
    return {"username": "user1"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    """Grab information about user by the username"""
    return {"username": username}
