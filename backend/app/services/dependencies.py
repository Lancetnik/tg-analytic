from typing import Optional

from fastapi import Depends
from fastapi.exceptions import HTTPException

from propan.config import settings

from config.dependencies import minio_session
from db.postgres.models import User
from db.postgres.channels import get_channel_or_none

from .schemas import Pagination


async def authorize():
    return await User.objects.first()


async def default_client(user: User = Depends(authorize)) -> Optional['client']:
    client = settings.CLIENTS.get_default(user.id)
    if client is None:
        raise HTTPException(status_code=401, detail="You have no default telegram account")
    else:
        return client


async def get_client(
    account: Optional[int],
    user: User = Depends(authorize)
) -> Optional['client']:
    client = settings.CLIENTS.get_client(user_id=user.id, account_id=account)
    if client is None:
        raise HTTPException(status_code=404, detail="There no such telegram account")
    else:
        return client


async def get_channel(channel: int):
    channel = await get_channel_or_none(pk=channel)
    if channel is None:
        raise HTTPException(status_code=404, detail="There no such channel")
    else:
        return channel


async def paginate(page: int = 1, size: int = 10):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page can not be less then 1")
    if size < 1:
        raise HTTPException(status_code=400, detail="Size can not be less then 1")
    return Pagination(page=page, size=size)


def minio():
    return minio_session.create_client(
        's3',
        endpoint_url=f'http://{settings.MINIO_HOST}:{settings.MINIO_PORT}',
        aws_access_key_id=settings.MINIO_USER,
        aws_secret_access_key=settings.MINIO_PASSWORD,
        use_ssl=False
    )
