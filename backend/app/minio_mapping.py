from propan.config import settings

from config.dependencies import minio_client


def check_bucket(bucket: str):
    if not minio_client.bucket_exists(bucket):
        minio_client.make_bucket(bucket)
        print(f"Bucket '{bucket}' created")
    else:
        print(f"Bucket '{bucket}' already exists")


if __name__ == '__main__':
    for i in [settings.PHOTO_BUCKET, settings.VIDEO_BUCKET]:
        check_bucket(i)