from datetime import datetime, timedelta
from functools import partial

from propan.config import settings

from config.dependencies import minio_client


async def get_file_url(filename: str, bucket: str) -> str:
    async with minio_client as client:
        return client.presigned_get_object(
            bucket_name=bucket,
            object_name=filename,
        )


async def put_file(filename: str, file: bytes, bucket: str) -> None:
    async with minio_client as client:
        client.put_object(Bucket=bucket, Key=filename, Body=file)


put_photo = partial(put_file, bucket=settings.PHOTO_BUCKET)
put_video = partial(put_file, bucket=settings.VIDEO_BUCKET)
