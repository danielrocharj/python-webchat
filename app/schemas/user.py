from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    active: Optional[bool] = True
    admin: Optional[bool] = False


class UserCreateRequest(UserBase):
    email: EmailStr
    username = str
    password: str


class User(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserInDB(User):
    password: str
