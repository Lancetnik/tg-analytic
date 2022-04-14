from fastapi import FastAPI

from propan.config import settings

from config.dependencies import es, redis

from db.postgres import connect_db, close_db
from db.postgres.channels import get_channel
from db.posts.schemas import ProcessStatus

from services.tg import add_listener
from tg.clients import TgClientRepository

from api import api_router
from index.router import html_router, static


app = FastAPI()
app.mount("/static", static, name="static")


@app.on_event("startup")
async def startup() -> None:
    await connect_db(rebuild=False)

    settings.CLIENTS = await TgClientRepository.create()

    for process in await ProcessStatus.get_monitorings():
        await add_listener(
            client=settings.CLIENTS.get_client(process.user_id, process.account_id),
            channel_link=(await get_channel(pk=process.channel_id)).link
        )


@app.on_event("shutdown")
async def shutdown() -> None:
    await close_db()
    await es.close()


app.include_router(html_router)
app.include_router(api_router)
