from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import PlainTextResponse, HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER

from app import crud
from app.dependencies import get_db
from app.security import validate_password, create_jwt_token, oauth2_scheme

router = APIRouter()
templates = Jinja2Templates(directory="./app/templates/")


def authenticate_user(username: str, password: str, db):
    user = crud.get_user_by_username(db, username)
    if not user or not validate_password(user.password, password):
        return None
    else:
        return user


@router.get("/echo")
async def ping():
    return PlainTextResponse("echo! echo! echo!")


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user_authenticated = authenticate_user(form_data.username, form_data.password, db)

    if not user_authenticated:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token(user_authenticated.username)

    response = RedirectResponse(url="/chat", status_code=HTTP_303_SEE_OTHER)
    response.set_cookie(key="Authorization", value=token)
    return response


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login/bots")
async def login_bots(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user_authenticated = authenticate_user(form_data.username, form_data.password, db)
    if not user_authenticated:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return create_jwt_token(user_authenticated.username)


@router.get("/")
async def index():
    return {"msg": "Python Webchat"}
