from typing import Optional

from telethon import TelegramClient, types, events
from telethon.sessions import StringSession


def create_client(api_id: int, api_hash: str, session: Optional[str] = None) -> TelegramClient:
    return TelegramClient(StringSession(session), api_id, api_hash)


async def start_client(api_id: int, api_hash: str, session: Optional[str] = None, phone: Optional[str] = None) -> TelegramClient:
    client = create_client(api_id, api_hash, session)
    if phone:
        return await client.start(phone)
    else:
        return await client.start()


async def get_channel(client, channel_link: str) -> types.Channel:
    return await client.get_entity(channel_link)


def add_channel_listener(client, channel, handler):
    client.add_event_handler(
        handler,
        events.NewMessage(incoming=True, from_users=[channel])
    )


def remove_channel_listener(client, channel, handler):
    client.remove_event_handler(
        handler,
        events.NewMessage(incoming=True, from_users=[channel])
    )
