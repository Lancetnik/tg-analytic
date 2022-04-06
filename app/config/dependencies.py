from elasticsearch import AsyncElasticsearch
from minio import Minio

from propan.config import settings


es = AsyncElasticsearch(
    hosts=[settings.ELASTIC_URL],
    http_auth=(settings.ELASTIC_USER, settings.ELASTIC_PASSWORD)
)

minio_client = Minio(
    f'{settings.MINIO_HOST}:{settings.MINIO_PORT}',
    access_key=settings.MINIO_USER,
    secret_key=settings.MINIO_PASSWORD,
    secure=False
)
