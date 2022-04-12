from fastapi import APIRouter

from . import ws, senders


api_router = APIRouter()
api_router.include_router(senders.router, tags=["Senders"])
api_router.include_router(ws.router, tags=["Websockets"])


__all__ = ('api_router',)