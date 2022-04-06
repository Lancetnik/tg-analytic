from fastapi import APIRouter, Depends, status, Response, BackgroundTasks

from loguru import logger

from db.postgres import database
from db.postgres.models import TgChannelProcess, Status, User
from db.postgres.channels import get_channel
from db.postgres.processes import (
    create_process, delete_process,
    get_processes, get_process
)
from services.dependencies import get_client, authorize, get_channel
from services.tg import add_listener, remove_listener, parse_channel


router = APIRouter(prefix="/process", tags=["process"])

BaseProcessResponse = TgChannelProcess.get_pydantic(include={
    "id": ...,
    "channel": {"id"},
    "account": {"id"},
    "last_change": ...,
    "status": ...
})


@router.post(
    "",
    response_model=BaseProcessResponse,
    status_code=status.HTTP_201_CREATED
)
@database.transaction()
async def start_monitoring_handler(
    account: int,
    channel = Depends(get_channel),
    client = Depends(get_client)
):
    process = await create_process(
        channel_id=channel.id, account_id=account, status=Status.monitoring.value
    )
    await add_listener(client, channel.link)
    return process


@router.post(
    "/history",
    response_model=BaseProcessResponse,
    status_code=status.HTTP_201_CREATED
)
@database.transaction()
async def start_history_handler(
    account: int,
    background_tasks: BackgroundTasks,
    channel = Depends(get_channel),
    client = Depends(get_client),
    pause: float = 0.3
):
    process = await create_process(
        channel_id=channel.id, account_id=account, status=Status.history.value
    )
    background_tasks.add_task(_history_process, process, client, channel.link, pause)
    return process


@router.delete(
    "/{process_id}",
    response_model=BaseProcessResponse,
    responses={204: {"model": None}},
)
@database.transaction()
async def delete_process_handler(process_id: int, user: User = Depends(authorize)):
    process = await delete_process(pk=process_id, account__user=user)

    if process is not None and process.status == Status.monitoring.value:
        channel = await get_channel(process.channel)
        client = await get_client(account=process.account.id, user=user)
        await remove_listener(client, channel.link)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/toggle/{process_id}",
    response_model=BaseProcessResponse
)
@database.transaction()
async def toggle_process_handler(
    process_id: int,
    status: Status,
    user: User = Depends(authorize),
):
    process = await get_process(pk=process_id, account__user=user)
    await process.update(status=status.value)

    channel = await get_channel(process.channel)
    client = await get_client(account=process.account.id, user=user)
    if status == Status.monitoring_stopped:
        await remove_listener(client, channel.link)
    elif status == Status.monitoring:
        await add_listener(client, channel.link)

    return process


@router.get(
    "",
    response_model=list[BaseProcessResponse]
)
async def get_processes_handler(user: User = Depends(authorize)):
    return await get_processes(account__user=user)


@router.get(
    "/{process_id}",
    response_model=BaseProcessResponse
)
async def get_process_handler(process_id: int, user: User = Depends(authorize)):
    return await get_process(pk=process_id, account__user=user)


async def _history_process(process, client, link, pause):
    try:
        await parse_channel(client, link, pause)
    except Exception as e:
        logger.error(f'Parsing channel {link} fault with {e}')
        await process.update(status=Status.error.value)
    else:
        await process.update(status=Status.history_done.value)


__all__ = ('router',)
