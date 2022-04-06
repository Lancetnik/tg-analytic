import io
from functools import partial

from propan.config import settings

from config.dependencies import minio_client


def put_file(filename: str, file: bytes, bucket: str) -> str:
    minio_client.put_object(bucket, filename, io.BytesIO(file), len(file))
    return minio_client.presigned_get_object(
        bucket_name=bucket,
        object_name=filename,
    )


put_photo = partial(put_file, bucket=settings.PHOTO_BUCKET)
put_video = partial(put_file, bucket=settings.VIDEO_BUCKET)
