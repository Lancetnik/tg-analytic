from telethon import TelegramClient, types, events


async def start_client(login: str, api_id: int, api_hash: str) -> TelegramClient:
    client = TelegramClient(login, api_id, api_hash)
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
