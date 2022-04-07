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
            {"datetime": {"order": "desc", "format": "strict_date_optional_time_nanos"}},
        ],
    )
