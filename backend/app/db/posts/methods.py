from typing import Optional

from elasticsearch import NotFoundError

from config.dependencies import es
from propan.config import settings


async def save_post(post: 'PostSchema') -> None:
    await es.index(
        index=settings.POSTS, document=post.dict(), id=post.message_id
    )


async def delete(post: 'PostSchema') -> None:
    await es.delete(
        index=settings.POSTS, id=post.message_id
    )


async def clear_all() -> None:
    await es.delete_by_query(
        index=settings.POSTS,
        query = {"match_all": {}, }
    )
    await es.delete_by_query(
        index=settings.PROCESSES,
        query = {"match_all": {}, }
    )


async def get_post(pk: int) -> 'PostSchema':
    try:
        return await es.get(index=settings.POSTS, id=pk)
    except NotFoundError:
        return None


async def get_posts(page: Optional[int] = None, size=10) -> list['PostSchema']:
    query = {"match_all": {}, }

    if page is not None:
        pagination = {
            'from_': (page-1)*size,
            'size': size
        }

    return await es.search(
        index=settings.POSTS,
        filter_path=['hits.hits._id', 'hits', 'hits.hits._source'],
        query=query,
        **pagination,
        sort=[
            {"published": {"order": "desc", "format": "strict_date_optional_time_nanos"}},
        ],
    )


async def save_status(status: 'ProcessStatus'):
    await es.index(
        index=settings.PROCESSES, document=status.dict(), id=status.task_id
    )


async def get_process(task_id=None) -> 'ProcessStatus':
    try:
        return await es.get(index=settings.PROCESSES, id=task_id)
    except NotFoundError:
        return None


async def find_process(user_id, account_id=None, channel_id=None, status=None) -> 'ProcessStatus':
    must = [{"match": { "user_id": user_id }}]
    if account_id: must.append({"match": { "account_id": account_id }})
    if channel_id: must.append({"match": { "channel_id": account_id }})
    if status: must.append({"match": { "status": status }})

    try:
        return (await es.search(
            index=settings.PROCESSES,
            filter_path=['hits.hits._id', 'hits', 'hits.hits._source'],
            query={"bool": { "must": must }},
            sort=[
                {"updated": {"order": "desc", "format": "strict_date_optional_time_nanos"}},
            ],
        ))['hits']['hits'][0]
    except IndexError:
        return None


async def delete_process(task_id: str):
    await es.delete(index=settings.PROCESSES, id=task_id)


async def get_processes(user_id=None, status=None, **kwargs) -> list['ProcessStatus']:
    must = []
    if user_id: must.append({"match": { "user_id": user_id }})
    if status: must.append({"match": { "status": status }})

    return await es.search(
        index=settings.PROCESSES,
        filter_path=['hits.hits._id', 'hits', 'hits.hits._source'],
        query={"bool": {"must": must}} if must else {"match_all": {}},
        sort=[
            {"updated": {"order": "desc", "format": "strict_date_optional_time_nanos"}},
        ],
    )
