import logging

import aioredis
from elasticsearch import AsyncElasticsearch
from aiobotocore.session import get_session
from uvicorn.config import logger

from propan.config import settings


es = AsyncElasticsearch(
    hosts=[settings.ELASTIC_URL],
    http_auth=(settings.ELASTIC_USER, settings.ELASTIC_PASSWORD)
)

minio_session = get_session()

redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

logger = logging.getLogger("uvicorn.error")
