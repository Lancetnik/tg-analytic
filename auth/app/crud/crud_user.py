from typing import Any, Optional, Union

from ormar.exceptions import NoMatch

from config.security import get_password_hash, verify_password
from db.models import User
from schemas.user import UserCreate, UserUpdate

from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, *, email: str) -> Optional[User]:
        try:
            return await User.objects.filter(email=email).first()
        except NoMatch:
            return None

    async def create(self, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        await db_obj.save()
        return db_obj

    async def update(
        self, *, db_obj: User, obj_in: Union[UserUpdate, dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, *, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
