import uvicorn
from fastapi import FastAPI
from app.models import user
from app.database import engine
from app.api import users, root

user.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Python Webchat")

app.include_router(root.router)
app.include_router(users.router, prefix="/users", tags=["users"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=5000)
