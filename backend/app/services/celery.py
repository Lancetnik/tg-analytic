import asyncio
from functools import wraps

from celery import Celery

from propan.config import settings

from config.dependencies import logger
from db.postgres import connect_db, close_db


celery = Celery(__name__)
celery.conf.broker_url = settings.REDIS_URL
celery.conf.result_backend = settings.REDIS_URL
loop = asyncio.new_event_loop()


def db(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await connect_db()
        try:
            return await func(*args, **kwargs)
        finally:
            await close_db()
    return wrapper


def async_to_sync(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return loop.run_until_complete(db(func)(*args, **kwargs))
    return wrapper
