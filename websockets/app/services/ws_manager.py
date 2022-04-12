from typing import Optional, Union

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.rooms: dict[str, list[WebSocket]] = {}
        self.users: dict[int, WebSocket] = {}


    async def connect(self, room: str, user_id: int, websocket: WebSocket):
        await websocket.accept()

        connections = self.rooms.get(room, [])
        connections.append(websocket)
        self.rooms[room] = connections

        self.users[user_id] = websocket


    def disconnect(self, room: str, user_id: int, websocket: WebSocket):
        try:
            self.rooms.get(room, []).remove(websocket)
        except ValueError:
            pass
        self.users.pop(user_id, None)


    async def send_personal_message(self, message: Union[str, dict], user_id: int):
        if (websocket := self.users.get(user_id)) is not None:
            if isinstance(message, str):
                await websocket.send_json({'message': message})
            elif isinstance(message, dict):
                await websocket.send_json(message)
            else:
                raise ValueError('message should be string or dict')


    async def broadcast(self, message: Union[str, dict], room: Optional[str] = None):
        if room is None:
            sockets = self.users.values()
        else:
            sockets = self.rooms.get(room, [])

        if isinstance(message, str):
            for connection in sockets:
                await connection.send_json({'message': message})

        elif isinstance(message, dict):
            for connection in sockets:
                await connection.send_json(message)

        else:
            raise ValueError('message should be string or dict')


manager = ConnectionManager()
