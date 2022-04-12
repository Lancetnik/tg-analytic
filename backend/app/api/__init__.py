from fastapi import APIRouter

from . import users, posts, accounts, channels, processes


api_router = APIRouter()
api_router.include_router(users.router, prefix="/user", tags=["Users"])
api_router.include_router(posts.router, prefix="/post", tags=["Posts"])
api_router.include_router(accounts.router, prefix="/account", tags=["Accounts"])
api_router.include_router(channels.router, prefix="/channel", tags=["Channels"])
api_router.include_router(processes.router, prefix="/process", tags=["Process"])


__all__ = ('api_router',)
