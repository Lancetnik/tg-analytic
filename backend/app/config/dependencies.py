import aioredis
from elasticsearch import AsyncElasticsearch
from aiobotocore.session import get_session

from propan.config import settings


es = AsyncElasticsearch(
    hosts=[settings.ELASTIC_URL],
    http_auth=(settings.ELASTIC_USER, settings.ELASTIC_PASSWORD)
)

minio_client = get_session().create_client(
    's3',
    endpoint_url=f'http://{settings.MINIO_HOST}:{settings.MINIO_PORT}',
    aws_access_key_id=settings.MINIO_USER,
    aws_secret_access_key=settings.MINIO_PASSWORD,
    use_ssl=False
)

redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
