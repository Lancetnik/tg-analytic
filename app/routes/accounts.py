from fastapi import APIRouter, status, Response, Depends

from db.postgres.models import TgUserAccount, User
from db.postgres.accounts import (
    get_account, get_accounts,
    delete_account, set_default,
    create_account
)
from services.dependencies import authorize


router = APIRouter(prefix="/account", tags=["accounts"])

BaseAccountResponse = TgUserAccount.get_pydantic(exclude={'user', 'processes'})
AccountCreate = TgUserAccount.get_pydantic(include={'api_hash', 'api_id', 'login'})


@router.post(
    "",
    response_model=BaseAccountResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_account_handler(
    account: AccountCreate,
    user: User = Depends(authorize)
):
    return await create_account(user=user.id, **account.dict())


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
