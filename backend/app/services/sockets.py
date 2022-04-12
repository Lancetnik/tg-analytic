import json

import grpc

from propan.config import settings
from .grpc import websockets_pb2, websockets_pb2_grpc


async def send_to_user(user_id: int, message):
    async with grpc.aio.insecure_channel(
        f'{settings.WEBSOCKETS_HOST}:{settings.WEBSOCKETS_PORT + 1}'
    ) as channel:
        stub = websockets_pb2_grpc.SenderStub(channel)
        response = await stub.SendMessage(websockets_pb2.Message(
            message=json.dumps({
                'cliend_id': user_id,
                'message': message
            })
        ))


async def send_to_group(group: str, message):
    async with grpc.aio.insecure_channel(
        f'{settings.WEBSOCKETS_HOST}:{settings.WEBSOCKETS_PORT + 1}'
    ) as channel:
        stub = websockets_pb2_grpc.SenderStub(channel)
        response = await stub.SendMessage(websockets_pb2.Message(
            message=json.dumps({
                'room': group,
                'message': message
            })
        ))
