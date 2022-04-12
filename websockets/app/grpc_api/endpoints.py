import json

import grpc

from services.ws_manager import manager
from .schema import websockets_pb2, websockets_pb2_grpc


class Sender(websockets_pb2_grpc.SenderServicer):
    async def SendMessage(
            self,
            request: websockets_pb2.Message,
            context: grpc.aio.ServicerContext) -> websockets_pb2.Reply:
        message = json.loads(request.message)

        if (client_id := message.get('cliend_id')) is not None:
            await manager.send_personal_message(message=message['message'], user_id=client_id)
            return websockets_pb2.Reply(message=f"Message `{message['message']}` was sended to user `{client_id}`")

        if (room := message.get('room')) is not None:
            await manager.broadcast(message=message['message'], room=room)
            return websockets_pb2.Reply(message=f"Message `{message['message']}` was sended to group `{room}`")
