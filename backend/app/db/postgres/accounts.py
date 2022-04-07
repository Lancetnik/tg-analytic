from typing import Optional

from fastapi.exceptions import HTTPException
from propan.config import settings

from . import database
from .models import TgUserAccount


async def get_accounts(**filters):
    return await TgUserAccount.objects.filter(**filters).all()


async def get_account_or_none(**params):
    return await TgUserAccount.objects.get_or_none(**params)


async def get_account(**params):
    account = await get_account_or_none(**params)
    if account is None:
        raise HTTPException(status_code=404)
    else:
        return account


@database.transaction()
async def delete_account(**params) -> bool:
    account = await get_account_or_none(**params)

    if account is None:
        return False
    
    else:
        await account.delete()
        await settings.CLIENTS.delete_account(
            user_id=account.user.id, account_id=account.id
        )
        return True


@database.transaction()
async def set_default(pk, user, **params):
    account = await get_account(pk=pk, user=user, **params)
    await TgUserAccount.objects.filter(user=user).update(default=False)
    await account.update(default=True)

    settings.CLIENTS.set_default(user_id=user, account_id=pk)
    return account


async def create_account(*args, **params):
    account = TgUserAccount(*args, **params)
    await account.save()
    return account
