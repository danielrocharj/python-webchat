import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud
from app.api import users, root
from app.config import settings
from app.database.core import engine, SessionLocal
from app.database.seeder import user_seeder
from app.dependencies import get_db
from app.models import user
from app.schemas.user import UserCreateRequest
from app.security import validate_password, oauth2_scheme, create_jwt_token

app = FastAPI(title="Python Webchat")

app.include_router(root.router)
app.include_router(users.router, prefix="/users", tags=["users"])


@app.on_event("startup")
def startup():
    user.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user_seeder(db)


def authenticate_user(username: str, password: str, db):
    user = crud.get_user_by_username(db, username)
    if not user or not validate_password(user.password, password):
        return None
    else:
        return user


@app.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user_authenticated = authenticate_user(form_data.username, form_data.password, db)

    if not user_authenticated:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token(user_authenticated.username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/access")
async def index(token: str = Depends(oauth2_scheme)):
    return {"the_token": token}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=5000)
