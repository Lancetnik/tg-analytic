from config.dependencies import logger
from db.postgres import accounts, processes
from db.postgres.models import Status

from services.celery import celery, async_to_sync
from services.tg import parse_channel as parse
from tg.methods import start_client


@celery.task(name="parse_channel")
@async_to_sync
async def parse_channel(process_id, account_id, link, pause):
    acc = await accounts.get_account(pk=account_id)
    client = await start_client(acc.api_id, acc.api_hash, acc.session)
    process = await processes.get_process(pk=process_id)

    try:
        await parse(client, link, pause)
    except Exception as e:
        logger.error(f'Parsing channel {link} fault with {e}')
        await process.update(status=Status.error.value)
    else:
        await process.update(status=Status.history_done.value)
    finally:
        await client.disconnect()
