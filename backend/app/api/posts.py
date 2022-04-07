import urllib

from fastapi import APIRouter, Request, Depends, status, Response

from db.posts.methods import get_posts
from db.posts.schemas import PaginatedPosts, PostSchema
from services.dependencies import paginate
from services.schemas import Pagination


router = APIRouter()


@router.get('', response_model=PaginatedPosts)
async def get_posts_handler(request: Request, filters: Pagination = Depends(paginate)):
    posts = await get_posts(filters.page, filters.size)
    data = PostSchema.list_from_elastic(posts)
    count = posts['hits']['total']['value']

    params = request._query_params._dict
    query = request.scope['raw_path'].decode()

    params['page'] = filters.page + 1
    if filters.size * filters.page < count:
        next = f'{query}?{urllib.parse.urlencode(params)}'
    else:
        next = None

    params['page'] = filters.page - 1
    if filters.page > 1:
        previous = f'{query}?{urllib.parse.urlencode(params)}'
    else:
        previous = None

    return {
        'next': next,
        'previous': previous,
        'count': count,
        'data': data
    }


@router.get('/{post_id}', response_model=PostSchema)
async def get_post_handler(post_id: int):
    post = await PostSchema.get_or_none(post_id)
    if post is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return post


__all__ = ('router',)
