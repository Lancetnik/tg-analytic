import asyncio
from functools import wraps

from celery import Celery
from celery.signals import celeryd_after_setup

from propan.config import settings

from db.postgres import connect_db


celery = Celery(__name__)
celery.conf.broker_url = settings.REDIS_URL
celery.conf.result_backend = settings.REDIS_URL
loop = asyncio.new_event_loop()


@celeryd_after_setup.connect
def init_celery(*agrs, **kwargs):
    loop.run_until_complete(connect_db(rebuild=False))


def async_to_sync(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return loop.run_until_complete(func(*args, **kwargs))
    return wrapper
