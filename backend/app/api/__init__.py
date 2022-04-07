from fastapi import APIRouter

from . import users, posts, accounts, channels, processes


api_router = APIRouter()
api_router.include_router(users.router, prefix="/user", tags=["users"])
api_router.include_router(posts.router, prefix="/post", tags=["posts"])
api_router.include_router(accounts.router, prefix="/account", tags=["accounts"])
api_router.include_router(channels.router, prefix="/channel", tags=["channels"])
api_router.include_router(processes.router, prefix="/process", tags=["process"])


__all__ = ('api_router',)
