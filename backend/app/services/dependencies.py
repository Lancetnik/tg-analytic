from typing import Optional

from fastapi import Depends
from fastapi.exceptions import HTTPException

from propan.config import settings

from config.dependencies import minio_session
from db.postgres.channels import get_channel_or_none
from db.posts.schemas import ProcessStatus

from .schemas import Pagination


async def authorize() -> 'user_id':
    return 1


async def default_client(user_id: int = Depends(authorize)) -> Optional['client']:
    client = settings.CLIENTS.get_default(user_id)
    if client is None:
        raise HTTPException(status_code=401, detail="You have no default telegram account")
    else:
        return client


async def get_client(
    account: Optional[int],
    user_id: int = Depends(authorize)
) -> Optional['client']:
    client = settings.CLIENTS.get_client(user_id=user_id, account_id=account)
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


async def get_task(task_id: str, user_id: int = Depends(authorize)):
    task = await ProcessStatus.get(user_id, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="There no such task")
    else:
        return task


async def get_client_by_task(task = Depends(get_task), user_id: int = Depends(authorize)):
    return await get_client(account=task.account_id, user_id=user_id)


async def get_task_channel(task = Depends(get_task)):
    return await get_channel(task.channel_id)


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
