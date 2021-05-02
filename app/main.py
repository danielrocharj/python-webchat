import uvicorn
from fastapi import FastAPI
from app.routes import users, root

app = FastAPI(title="Python Webchat")
app.include_router(root.router)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=5000)
