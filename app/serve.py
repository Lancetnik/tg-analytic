from fastapi import FastAPI

from propan.config import settings

from config.dependencies import es

from db.postgres import connect_db, close_db
from db.postgres.processes import get_monitorings
from db.postgres.channels import get_channel

from services.tg import add_listener
from tg.clients import TgClientRepository

from routes import routes


app = FastAPI()


@app.on_event("startup")
async def startup() -> None:
    await connect_db(rebuild=False)

    settings.CLIENTS = await TgClientRepository.create()

    for process in await get_monitorings():
        await add_listener(
            client=settings.CLIENTS.get_client(process.account.user.id, process.account.id),
            channel_link=(await get_channel(pk=process.channel.id)).link
        )


@app.on_event("shutdown")
async def shutdown() -> None:
    await close_db()
    await es.close()


for route in routes:
    app.include_router(route)
