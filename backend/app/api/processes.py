from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException

from db.posts.schemas import ProcessStatus, Status
from services.dependencies import (
    get_client, authorize, get_channel,
    get_task, get_client_by_task, get_task_channel
)
from services.tg import add_listener, remove_listener
from worker import parse_channel, kill_task


router = APIRouter()


@router.get(
    "",
    response_model=list[ProcessStatus]
)
async def get_processes_handler(user_id: int = Depends(authorize)):
    return await ProcessStatus.list(user_id=user_id)


@router.get(
    "/{task_id}",
    response_model=ProcessStatus
)
async def check_task_state(
    task_id: str,
    user_id: int = Depends(authorize),
):
    return await ProcessStatus.get(user_id=user_id, task_id=task_id)


@router.post(
    "",
    response_model=ProcessStatus,
    status_code=status.HTTP_201_CREATED
)
async def start_monitoring_handler(
    account: int,
    client = Depends(get_client),
    channel = Depends(get_channel),
    user_id: int = Depends(authorize)
):
    process = await ProcessStatus(
        account_id=account, user_id=user_id,
        channel_id=channel.id, status=Status.monitoring.value
    ).save()
    await add_listener(client, channel.link)
    return process


@router.post(
    "/history",
    response_model=ProcessStatus,
    status_code=status.HTTP_201_CREATED
)
async def start_history_handler(
    account: int,
    channel = Depends(get_channel),
    client = Depends(get_client),
    user_id: int = Depends(authorize),
    pause: float = 0.3
):
    if (p := await ProcessStatus.find(
        user_id=user_id,
        channel_id=channel.id,
        status=Status.history.value)
    ):
        raise HTTPException(
            status_code=400,
            detail=f"`{channel.link}` already parsing at task `{p.task_id}`"
        )

    process = ProcessStatus(
        account_id=account, channel_id=channel.id,
        user_id=user_id, status=Status.history.value
    )
    task = parse_channel.delay(account, channel.id, pause)
    process.task_id = task.id
    return process


@router.patch(
    "/toggle/{process_id}",
    response_model=ProcessStatus
)
async def toggle_process_handler(
    status: Status,
    user_id: int = Depends(authorize),
    task: ProcessStatus = Depends(get_task),
    client = Depends(get_client_by_task),
    channel = Depends(get_task_channel)
):
    process = task

    if process.status == Status.history and status != Status.history:
        kill_task(process.task_id)

    if status == Status.monitoring_stopped:
        process = await task.update(status=status.value)
        await remove_listener(client, channel.link)

    elif status == Status.monitoring:
        process = await task.update(status=status.value)
        await add_listener(client, channel.link)

    elif status == Status.history:
        if (p := await ProcessStatus.find(
            user_id=user_id,
            channel_id=channel.id,
            status=Status.history.value)
        ):
            raise HTTPException(
                status_code=400,
                detail=f"`{channel.link}` already parsing at task `{p.task_id}`"
            )

        if process.status == Status.history_stopped \
        or process.status == Status.error:
            await process.delete()

        task = parse_channel.delay(task.account_id, channel.id)
        process = await process.update(status=status.value, task_id=task.id)
    
    elif status == Status.history_stopped:
        process = await process.update(status=Status.history_stopped.value)

    return process


__all__ = ('router',)
