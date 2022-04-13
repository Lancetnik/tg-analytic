from celery.result import AsyncResult
from celery.exceptions import Ignore
from fastapi.exceptions import HTTPException

from config.dependencies import logger
from db.postgres import accounts, channels
from db.posts.schemas import Status, ProcessStatus

from services.celery import celery, async_to_sync
from services.tg import parse_channel as parse
from tg.methods import start_client


@celery.task(name="parse_channel", bind=True)
@async_to_sync
async def parse_channel(self, account_id, channel_id, pause=0.1):
    acc = await accounts.get_account(pk=account_id)
    client = await start_client(acc.api_id, acc.api_hash, acc.session)
    channel = await channels.get_channel(pk=channel_id)

    task = await ProcessStatus(
        account_id=account_id, channel_id=channel.id,
        user_id=acc.user.id, status=Status.history.value,
        task_id=self.request.id
    ).save()

    try:
        await parse(client, channel.link, pause)
    except Exception as e:
        logger.error(f'Parsing channel {channel.link} fault with {e}')
        await task.update(status=Status.error.value)
    else:
        await task.update(status=Status.history_done.value)
    finally:
        await client.disconnect()
    raise Ignore()
