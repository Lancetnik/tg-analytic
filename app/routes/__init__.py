from .users import router as user_router
from .posts import router as post_router
from .accounts import router as account_router
from .channels import router as channel_router
from .processes import router as process_router


routes = (
    user_router, post_router,
    account_router, channel_router,
    process_router
)


__all__ = ('routes',)
