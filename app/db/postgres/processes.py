from asyncpg.exceptions import ForeignKeyViolationError
from fastapi.exceptions import HTTPException

from db.postgres.models import TgChannelProcess, Status


async def create_process(channel_id: int, account_id: int, status: str):
    try:
        return await TgChannelProcess(
            channel=channel_id, account=account_id, status=status
        ).save()
    except Exception:
        raise HTTPException(status_code=400)


async def get_processes(**filters):
    return await TgChannelProcess.objects.filter(**filters).all()


async def get_monitorings(**filters):
    return await TgChannelProcess.objects\
        .prefetch_related('account__user')\
        .filter(**filters)\
        .filter(status=Status.monitoring.value)\
        .all()


async def get_process_or_none(**params):
    return await TgChannelProcess.objects.get(**params)


async def get_process(**params):
    process = await get_process_or_none(**params)
    if process is None:
        raise HTTPException(status_code=404)
    else:
        return process


async def delete_process(**params):
    process = await get_process_or_none(**params)

    if process is None:
        return None
    
    else:
        await process.delete()
        return process
