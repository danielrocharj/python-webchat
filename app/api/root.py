from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/")
async def root():
    return {"msg": "Python Webchat"}


@router.get("/echo")
async def ping():
    return PlainTextResponse("echo! echo! echo!")
