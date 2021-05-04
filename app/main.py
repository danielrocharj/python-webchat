import uvicorn
from fastapi import FastAPI
from app.api import users, root, chat
from app.database.core import engine, SessionLocal
from app.database.seeder import user_seeder
from app.models import user


app = FastAPI(title="Python Webchat")

app.include_router(root.router)
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(chat.chat_router)


@app.on_event("startup")
def startup():
    user.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user_seeder(db)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=5000)
