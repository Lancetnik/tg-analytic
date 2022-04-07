import asyncio

from telethon import events, types
from loguru import logger

from config.dependencies import redis
from db.posts import PostSchema
from db.postgres.accounts import get_account
from db.minio import put_photo, put_video
from tg.methods import (
    add_channel_listener, remove_channel_listener,
    get_channel, create_client
)


async def parse_message(client, account_id, message):
    photo, video = None, None

    if message.photo is not None:
        photo = await client.download_media(message=message, file=bytes)
        name = f'{message.video.id}-{message.id}-{message.date}.jpg'
        await put_photo(name, photo)
    
    if message.video is not None:
        video = await client.download_media(message=message, file=bytes)
        name = f'{message.video.id}-{message.id}-{message.date}.mp4'
        await put_video(name, video)

    post = PostSchema.from_tg(
        account_id=account_id,
        message=message,
        photos=[name] if photo else [],
        videos=[name] if video else []
    )
    logger.info(post)
    await post.save()
    return post


async def event_handler(event: events.NewMessage):
    account = await get_account(
        api_id=event._client.api_id, api_hash=event._client.api_hash
    )
    await parse_message(
        client=event._client,
        account_id=account.id,
        message=event.message
    )


async def parse_channel(client, channel_link: str, pause = 0.1):
    logger.info(f'Parsing channel {channel_link} started')

    account = await get_account(
        api_id=client.api_id, api_hash=client.api_hash
    )
    channel = await get_channel(client, channel_link)

    async for message in client.iter_messages(channel):
        await parse_message(client, account.id, message)
        await asyncio.sleep(pause)
    
    logger.success(f'Parsing channel {channel_link} done')


async def add_listener(client, channel_link: str):
    logger.info(f'Monitoring at channel {channel_link} started')
    channel = await get_channel(client, channel_link)
    add_channel_listener(client, channel, event_handler)


async def remove_listener(client, channel_link: str):
    logger.info(f'Monitoring at channel {channel_link} stopped')
    channel = await get_channel(client, channel_link)
    remove_channel_listener(client, channel, event_handler)


from loguru import logger
async def send_phone_code(account):
    client = create_client(account.api_id, account.api_hash)
    await client.start()
    
    await client.connect()
    
    await client.send_code_request(account.phone)

    code_hash = client._phone_code_hash[account.phone]
    session=client.session.save()
    
    await redis.hset(account.id, mapping={
        'session': session,
        'code_hash': code_hash
    })
    logger.debug(await redis.hgetall(account.id))

    await client.disconnect()


async def verify_account(account, code):
    data = await redis.hgetall(account.id)
    logger.debug(data)

    client = create_client(account.api_id, account.api_hash, session=data['session'])
    await client.connect()

    await client.sign_in(phone=account.phone, code=code, phone_code_hash=data['code_hash'])

    await account.update(session=client.session.save(), activated=True)
    await client.disconnect()