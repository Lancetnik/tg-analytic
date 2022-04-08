from typing import Optional
from fastapi import APIRouter, status, Response, Depends, Body

from propan.config import settings

from db.postgres import database
from db.postgres.models import TgUserAccount, User
from db.postgres.accounts import (
    get_account, get_accounts,
    delete_account, set_default,
    create_account
)
from services.dependencies import authorize
from services.tg import send_phone_code, verify_account


router = APIRouter()

BaseAccountResponse = TgUserAccount.get_pydantic(
    exclude={'user', 'processes', 'session'}
)


@router.post(
    "",
    response_model=BaseAccountResponse,
    status_code=status.HTTP_201_CREATED
)
@database.transaction()
async def create_account_handler(
    api_id: int = Body(...),
    api_hash: str = Body(...),
    phone: str = Body(...),
    user: User = Depends(authorize)
):
    account = await create_account(
        user=user.id, phone=phone,
        api_id=api_id, api_hash=api_hash
    )
    await send_phone_code(account)
    return account



@router.post(
    "/confirm",
    response_model=BaseAccountResponse,
    status_code=status.HTTP_201_CREATED
)
@database.transaction()
async def confirm_account_handler(
    account_id: int,
    code: int,
    user: User = Depends(authorize)
):
    account = await get_account(pk=account_id, user=user.id)
    await verify_account(account, code)
    await settings.CLIENTS.create_account(account)
    return account



@router.patch(
    "/default/{account_id}",
    response_model=BaseAccountResponse
)
async def account_set_default_handler(
    account_id: int,
    user: User = Depends(authorize)
):
    return await set_default(pk=account_id, user=user.id)


@router.get(
    "",
    response_model=list[BaseAccountResponse]
)
async def get_accounts_handler(user: User = Depends(authorize)):
    return await get_accounts(user=user.id)


@router.get(
    "/{account_id}",
    response_model=BaseAccountResponse
)
async def get_account_handler(
    account_id: int,
    user: User = Depends(authorize)
):
    return await get_account(pk=account_id, user=user.id)


@router.delete(
    "/{account_id}",
    response_model=BaseAccountResponse,
    responses={204: {"model": None}},
)
async def delete_account_handler(
    account_id: int,
    user: User = Depends(authorize)
):
    await delete_account(pk=account_id, user=user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


__all__ = ('router',)
