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
    activated: bool = ormar.Boolean(default=False)

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


class Status(str, Enum):
    monitoring = "MONITORING"
    history = "PARSING"
    monitoring_stopped = "MONITORING-STOPPED"
    history_stopped = "PARSING-STOPPED"
    history_done= "PARSING-DONE"
    error = "ERROR"


class TgChannelProcess(ormar.Model):
    class Meta(BaseMeta):
        tablename = "channel_process"
        constraints = [ormar.UniqueColumns("channel", "account", "status")]

    id: int = ormar.Integer(primary_key=True)
    channel: TgChannel = ormar.ForeignKey(
        TgChannel, nullable=False, related_name='processes'
    )
    account: TgUserAccount = ormar.ForeignKey(
        TgUserAccount, nullable=False, related_name='processes'
    )
    created: datetime = ormar.DateTime(default=lambda: datetime.now())
    changed: datetime = ormar.DateTime(default=lambda: datetime.now())
    status: str = ormar.Text(choices=tuple(i.value for i in  Status))

    async def update(self, **params):
        await super().update(**params, changed=datetime.now())

    def __hash__(self):
        return hash(self.id)
