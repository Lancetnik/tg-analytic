from datetime import datetime, timedelta
from functools import partial

from propan.config import settings

from services.dependencies import minio


async def get_file_url(filename: str, bucket: str) -> str:
    async with minio() as client:
        return await client.presigned_get_object(
            bucket_name=bucket,
            object_name=filename,
        )


async def put_file(filename: str, file: bytes, bucket: str) -> None:
    async with minio() as client:
        await client.put_object(Bucket=bucket, Key=filename, Body=file)


put_photo = partial(put_file, bucket=settings.PHOTO_BUCKET)
put_video = partial(put_file, bucket=settings.VIDEO_BUCKET)
