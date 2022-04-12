from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from services.ws_manager import manager


router = APIRouter()


@router.websocket("/ws/{room_key}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_key: str, user_id: int):
    await manager.connect(room=room_key, user_id=user_id, websocket=websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(room=room_key, user_id=user_id, websocket=websocket)

