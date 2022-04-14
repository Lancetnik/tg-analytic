from celery.contrib.abortable import AbortableTask, AbortableAsyncResult
from celery.exceptions import Ignore

from config.dependencies import logger
from db.postgres import accounts, channels
from db.posts.schemas import Status, ProcessStatus

from services.celery import celery, async_to_sync
from services.tg import parse_channel as parse, parse_message
from tg.methods import start_client


@celery.task(name="parse_channel", bind=True, base=AbortableTask)
@async_to_sync
async def parse_channel(self, account_id, channel_id, pause=0.1):
    acc = await accounts.get_account(pk=account_id)

    if (task := await ProcessStatus.find(user_id=acc.user_id, status=Status.history.value)):
        logger.info(f'Parsing channel {channel_id} already running by user {acc.user_id}')
        raise Ignore()

    client = await start_client(acc.api_id, acc.api_hash, acc.session)
    channel = await channels.get_channel(pk=channel_id)

    task = await ProcessStatus(
        account_id=account_id, channel_id=channel.id,
        user_id=acc.user_id, status=Status.history.value,
        task_id=self.request.id
    ).save()

    try:
        async for message in parse(client, channel.link, pause):
            if self.is_aborted() is True:
                raise Ignore()

            await parse_message(client, acc.id, message)

    except Ignore:
        logger.info(f'Parsing channel {channel.link} stopped')
        await task.update(status=Status.history_stopped.value)
        
    except Exception as e:
        logger.error(f'Parsing channel {channel.link} fault with {e}')
        await task.update(status=Status.error.value)

    else:
        logger.info(f'Parsing channel {channel.link} done')
        await task.update(status=Status.history_done.value)

    finally:
        await client.disconnect()


def kill_task(task_id: str, wait: bool = True):
    task = AbortableAsyncResult(task_id)
    if is_task_running(task_id) and not task.is_aborted():
        task.abort()
        if wait is True:
            task.get()


def is_task_running(task_id):
    apps_dict = celery.control.inspect().active()
    if apps_dict:
        for worker, tasks in apps_dict.items():
            for task in tasks:
                if task_id == task['id']:
                    return True
    return False
