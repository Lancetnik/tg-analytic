import asyncio

from propan.config import settings

from services.dependencies import minio


async def check_bucket(bucket_name: str):
    async with minio() as client:
        if bucket_name not in {i['Name'] for i in (await client.list_buckets())['Buckets']}:
            await client.create_bucket(Bucket=bucket_name)
            print(f'Bucket `{bucket_name}` created!')
        else:
            print(f'Bucket `{bucket_name}` already exists!')


if __name__ == '__main__':
    for i in [settings.PHOTO_BUCKET, settings.VIDEO_BUCKET]:
        asyncio.run(check_bucket(i))