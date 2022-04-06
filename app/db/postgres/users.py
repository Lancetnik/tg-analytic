from fastapi.exceptions import HTTPException

from . import database
from .models import User


async def get_users(**filters):
    return await User.objects.filter(**filters).all()


async def get_users_with_accounts(**filters):
    return await User.objects.prefetch_related('accounts').filter(**filters).all()


async def get_user_or_none(**params):
    return await User.objects.get_or_none(**params)


async def get_user(**params):
    user = await get_user_or_none(**params)
    if user is None:
        raise HTTPException(status_code=404)
    else:
        return user


@database.transaction()
async def delete_user(**params) -> bool:
    user = await get_user_or_none(**params)

    if user is None:
        return False
    
    else:
        await user.accounts.queryset.delete()
        await user.delete()
        return True
