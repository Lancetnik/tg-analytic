import databases
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine

from propan.config import settings
from propan.logger import loguru as logger


database = databases.Database(settings.DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = create_async_engine(settings.DATABASE_URL, echo=True)


async def connect_db(rebuild: bool = False):
    if rebuild is True:
        async with engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)

    try:
        if not database.is_connected:
            await database.connect()
    except Exception as e:
        logger.error(f"connect db error, res is  {e}")
        await asyncio.sleep(3)
        asyncio.ensure_future(connect_db())
    else:
        logger.success("DB connected")


async def close_db():
    if database.is_connected:
        await database.disconnect()
