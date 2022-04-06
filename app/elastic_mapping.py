import asyncio
from functools import wraps
from pprint import pprint

from propan.config import settings

from config.dependencies import es
from db.posts import POSTS_MAPPING


def close_es(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        finally:
            await es.close()
    return wrapper


@close_es
async def create_scheme():
    try:
        await es.indices.delete(index=settings.POSTS)
    except Exception:
        pass

    pprint(await es.indices.create(index=settings.POSTS, mappings={
        "properties": POSTS_MAPPING
    }))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(create_scheme())
    loop.close()
