from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from . import methods


class PostSchema(BaseModel):
    account_id: int

    message_id: int
    chat_id: int
    published: datetime
    text: Optional[str]

    views: Optional[list[int]]
    forwards: Optional[list[int]]
    replies: Optional[list[int]]

    photos: Optional[list[str]]
    videos: Optional[list[str]]

    @classmethod
    def from_tg(cls, account_id: int, message, photos=[], videos=[]) -> 'PostSchema':
        return cls(
            account_id=account_id,
            message_id=message.id,
            chat_id=message._chat.id,
            published=message.date,
            text=message.text,
            views=[message.views or 0],
            forwards=[message.forwards or 0],
            replies=[message.replies.replies or 0 if message.replies else 0],
            photos=photos,
            videos=videos
        )


    @classmethod
    def from_elastic(cls, es_item: dict) -> 'PostSchema':
        return cls(**es_item['_source'])

    
    @classmethod
    def list_from_elastic(cls, es_items: dict) -> list['PostSchema']:
        return list(map(cls.from_elastic, es_items['hits']['hits']))


    async def save(self) -> 'PostSchema':
        await methods.save_post(self)
        return self

    
    async def delete(self) -> None:
        await methods.delete(self)


    @classmethod
    async def get(cls, pk: int) -> 'PostSchema':
        post = await methods.get_post(pk)
        return cls.from_elastic(post)


    @classmethod
    async def get_or_none(cls, pk: int) -> 'PostSchema':
        post = await methods.get_post(pk)
        if post is not None:
            return cls(**post['_source'])
        else:
            return None


    @classmethod
    async def list(cls, page=1, size=10, **kwargs) -> list['PostSchema']:
        request = await methods.get_posts(page, size, **kwargs)
        return cls.list_from_elastic(request)


    @staticmethod
    async def clear_all() -> None:
        await methods.clear_all()


class PaginatedPosts(BaseModel):
    next: Optional[str]
    previous: Optional[str]
    count: int
    data: list[PostSchema]


class Status(str, Enum):
    monitoring = "MONITORING"
    history = "PARSING"
    monitoring_stopped = "MONITORING-STOPPED"
    history_stopped = "PARSING-STOPPED"
    history_done= "PARSING-DONE"
    error = "ERROR"


class ProcessStatus(BaseModel):
    account_id: int
    user_id: int
    channel_id: int
    status: Status

    task_id: str = Field(default_factory=lambda: str(uuid4()))
    updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:  
        use_enum_values = True

    async def save(self) -> 'ProcessStatus':
        await methods.save_status(self)
        return self

    async def delete(self):
        return await methods.delete_process(self.task_id)

    @classmethod
    async def get_or_create(cls,
        account_id: int, user_id: int,
        channel_id: int, status: str
    ) -> ('ProcessStatus', bool):
        post = await methods.find_process(
            account_id=account_id,
            user_id=user_id,
            channel_id=channel_id,
            status=status
        )
        if post is None:
            return await self.save(), True
        return cls.from_elastic(post), False

    @classmethod
    def from_elastic(cls, es_item: dict) -> 'ProcessStatus':
        return cls(**es_item['_source'])
    
    @classmethod
    def list_from_elastic(cls, es_items: dict) -> list['ProcessStatus']:
        return list(map(cls.from_elastic, es_items['hits']['hits']))
    
    @classmethod
    async def get(cls, user_id: str, task_id: str) -> 'ProcessStatus':
        post = await methods.get_process(task_id)
        process = cls.from_elastic(post)
        if user_id == process.user_id:
            return process
        else:
            return None
    
    async def update(self, **params):
        data = self.dict()
        data.update(params)
        return await ProcessStatus(**data).save()

    @classmethod
    async def list(cls, **kwargs) -> list['ProcessStatus']:
        request = await methods.get_processes(**kwargs)
        return cls.list_from_elastic(request)

    @classmethod
    async def get_monitorings(cls):
        return await cls.list(status=Status.monitoring.value)
