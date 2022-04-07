from fastapi.exceptions import HTTPException

from .models import TgChannel


async def get_channels(**filters):
    return await TgChannel.objects.filter(**filters).all()


async def get_channel_or_none(**params):
    return await TgChannel.objects.get_or_none(**params)


async def get_channel(**params):
    channel = await get_channel_or_none(**params)
    if channel is None:
        raise HTTPException(status_code=404)
    else:
        return channel


async def delete_channel(**params) -> bool:
    channel = await get_channel_or_none(**params)

    if channel is None:
        return False
    
    else:
        await channel.delete()
        return True
