from datetime import datetime
from enum import Enum

import ormar
from sqlalchemy.sql import func

from . import metadata, database


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.Text()

    def __hash__(self):
        return hash(self.id)


class TgUserAccount(ormar.Model):
    class Meta(BaseMeta):
        tablename = "tg_account"

    id: int = ormar.Integer(primary_key=True)

    session: str = ormar.Text(nullable=True)
    phone: str = ormar.Text(lenght=32)
    api_id: int = ormar.Integer(unique=True)
    api_hash: str = ormar.Text(length=32, unique=True)

    user: User = ormar.ForeignKey(
        User, nullable=False, related_name='accounts'
    )
    default: bool = ormar.Boolean(default=False)

    def __hash__(self):
        return hash(self.id)


class TgChannel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "channel"

    id: int = ormar.BigInteger(primary_key=True)
    link: str = ormar.Text(unique=True)
    title: str = ormar.Text()

    def __hash__(self):
        return hash(self.id)
