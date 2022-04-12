from typing import Union

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from services.ws_manager import manager


router = APIRouter()


@router.post("/user", response_class=JSONResponse)
async def send_message_to_user(
    user_id: int = Body(...),
    message: Union[str, dict] = Body(...)
):
    await manager.send_personal_message(message, user_id)
    return {
        "user_id": user_id,
        "message": message
    }


@router.post("/room", response_class=JSONResponse)
async def send_message_to_room(
    room: str = Body(...),
    message: Union[str, dict] = Body(...)
):
    await manager.broadcast(message, room)
    return {
        "user_id": room,
        "message": message
    }
