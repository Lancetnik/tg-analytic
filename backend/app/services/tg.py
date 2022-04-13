import asyncio

import click
from telethon import events, types

from config.dependencies import redis, logger
from db.posts import PostSchema
from db.postgres import database
from db.postgres.accounts import get_account, get_accounts, set_default
from db.minio import put_photo, put_video
from tg.methods import (
    add_channel_listener, remove_channel_listener,
    get_channel, create_client
)


async def parse_message(client, account_id, message):
    photo, video = None, None

    if message.photo is not None:
        photo = await client.download_media(message=message, file=bytes)
        name = f'{message.photo.id}-{message.id}-{message.date}.jpg'
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


async def parse_channel(client, channel_link: str, pause = 0):
    logger.info(f'Parsing channel {channel_link} started')

    account = await get_account(
        api_id=client.api_id, api_hash=client.api_hash
    )

    channel = await get_channel(client, channel_link)

    async for message in client.iter_messages(channel):
        yield message
        await asyncio.sleep(pause)
    
    logger.info(f'Parsing channel {channel_link} done')


async def add_listener(client, channel_link: str):
    message =  "Monitoring at channel %s %s"
    color_message = f"Monitoring at channel {click.style('%s', bold=True)} {click.style('%s', fg='green')}"
    logger.info(message, channel_link, "started", extra={"color_message": color_message})

    channel = await get_channel(client, channel_link)
    add_channel_listener(client, channel, event_handler)


async def remove_listener(client, channel_link: str):
    message =  "Monitoring at channel %s %s"
    color_message = f"Monitoring at channel {click.style('%s', bold=True)} {click.style('%s', fg='red')}"
    logger.info(message, channel_link, "stopped", extra={"color_message": color_message})

    channel = await get_channel(client, channel_link)
    remove_channel_listener(client, channel, event_handler)


async def send_phone_code(account):
    client = create_client(account.api_id, account.api_hash)    
    await client.connect()

    await client.send_code_request(account.phone)

    code_hash = client._phone_code_hash[account.phone]
    session=client.session.save()
    
    await redis.hset(account.id, mapping={
        'session': session,
        'code_hash': code_hash
    })

    await client.disconnect()


@database.transaction()
async def verify_account(account, code):
    data = await redis.hgetall(account.id)

    client = create_client(account.api_id, account.api_hash, session=data['session'])
    await client.connect()

    await client.sign_in(phone=account.phone, code=code, phone_code_hash=data['code_hash'])

    if not await get_accounts(default=True, user=account.user):
        await set_default(account.id, account.user.id)

    await account.update(session=client.session.save())
    await client.disconnect()
