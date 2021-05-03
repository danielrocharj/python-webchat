import uvicorn
from fastapi import FastAPI

from app.models import user
from app.database.core import engine
from app.api import users, root

app = FastAPI(title="Python Webchat")

app.include_router(root.router)
app.include_router(users.router, prefix="/users", tags=["users"])


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=5000)
