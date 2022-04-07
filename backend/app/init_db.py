import asyncio

from db.postgres import connect_db

from db.postgres.models import *


asyncio.run(connect_db(rebuild=True))
