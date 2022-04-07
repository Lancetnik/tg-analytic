from fastapi import APIRouter, status
from fastapi.responses import Response

from db.postgres.models import User
from db.postgres.users import get_users, get_user, delete_user


router = APIRouter()

BaseUserResponse = User.get_pydantic(exclude={'accounts',})
UserCreate = User.get_pydantic(exclude={'accounts', 'id'})


@router.post(
    "",
    response_model=BaseUserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user_handler(user: UserCreate):
    return await User(**user.dict()).save()


@router.get(
    "",
    response_model=list[BaseUserResponse]
)
async def get_users_handler():
    return await get_users()


@router.get(
    "/{user_id}",
    response_model=User
)
async def get_user_handler(user_id: int):
    return await get_user(id=user_id)


@router.delete(
    "/{user_id}",
    response_model=BaseUserResponse,
    responses={204: {"model": None}},
)
async def delete_user_handler(user_id: int):
    await delete_user(id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


__all__ = ('router',)
