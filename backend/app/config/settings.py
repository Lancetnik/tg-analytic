from propan.config import settings


POSTS = 'posts'
PROCESSES = "processes"

ELASTIC_URL = f'{settings.ELASTIC_SCHEME}://{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}'

DATABASE_URL = f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}\
@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'

REDIS_URL = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"

PHOTO_BUCKET = 'tg-photo-bucket'
VIDEO_BUCKET = 'tg-video-bucket'
