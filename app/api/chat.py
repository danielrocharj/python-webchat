from typing import Optional

from fastapi import (
    APIRouter,
    Request,
    WebSocket,
    WebSocketDisconnect,
    Query,
    Depends,
    Cookie,
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette import status

from app.manager import ws_manager
from app.security import decode_jwt_token

chat_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Optional[str] = Cookie(None),
    token: Optional[str] = Query(None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@chat_router.get("/chat", response_class=HTMLResponse)
def route(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@chat_router.websocket("/ws/chat")
async def websocket_endpoint(
    websocket: WebSocket, token: str = Depends(get_cookie_or_token)
):
    user = decode_jwt_token(token)
    username = user["username"]
    await ws_manager.connect(websocket)
    data = f"{username} entered the room"
    await ws_manager.broadcast(data)
    try:
        while True:
            data = await websocket.receive_text()

            await ws_manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        await ws_manager.broadcast(f"{username} left the room")
