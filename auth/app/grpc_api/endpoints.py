import logging

import grpc
from propan.config import settings
from pydantic import ValidationError
from jose import jwt

import crud, schemas
from config import security
from .schema import auth_pb2, auth_pb2_grpc


logger = logging.getLogger("uvicorn.error")


class Checker(auth_pb2_grpc.CheckerServicer):
    async def CheckToken(
            self,
            request: auth_pb2.Token,
            context: grpc.aio.ServicerContext) -> auth_pb2.Reply:
        try:
            payload = jwt.decode(
                request.token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
            token_data = schemas.TokenPayload(**payload)
        except (jwt.JWTError, ValidationError):
            logger.info(f'GRPC: check token `{request.token}` fault')
            return auth_pb2.Reply(user_id=0)

        user = await crud.user.get(id=token_data.sub)
        if not user:
            logger.info(f'GRPC: check token `{request.token}` fault')
            return auth_pb2.Reply(user_id=0)

        logger.info(f'GRPC: check token `{request.token}` success - user `{user.id}`')
        return auth_pb2.Reply(user_id=user.id)
