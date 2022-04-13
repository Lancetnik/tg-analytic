import grpc

from propan.config import settings

from .grpc import auth_pb2, auth_pb2_grpc


async def check_token(token: str) -> int:
    async with grpc.aio.insecure_channel(
        f'{settings.AUTH_HOST}:{settings.AUTH_PORT}'
    ) as channel:
        stub = auth_pb2_grpc.CheckerStub(channel)
        response = await stub.CheckToken(auth_pb2.Token(
            token=token
        ))
    return response.user_id
