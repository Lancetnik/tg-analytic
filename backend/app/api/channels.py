from fastapi import APIRouter, status, Response, Depends
from fastapi.exceptions import HTTPException

from db.postgres.models import TgChannel
from db.postgres.channels import (
    get_channel, get_channel_or_none,
    get_channels, delete_channel
)

from services.dependencies import default_client
from tg.methods import get_channel as get_channel_data


router = APIRouter()

BaseChannelResponse = TgChannel.get_pydantic(exclude={'processes',})
ChannelLink = TgChannel.get_pydantic(include={'link'})


@router.post(
    "",
    response_model=BaseChannelResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_channel_handler(
    link: ChannelLink,
    client = Depends(default_client)
):
    link = link.link
    try:
        channel = await get_channel_or_none(link=link)
        channel_data = await get_channel_data(client, link)

        if channel is None:
            channel = await TgChannel(
                id=channel_data.id,
                title=channel_data.title,
                link=link
            ).save()
        else:
            await channel.update(title = channel_data.title)

        return channel

    except Exception as e:
        raise HTTPException(status_code=400, detail="Wrong channel link")


@router.get(
    "",
    response_model=list[BaseChannelResponse]
)
async def get_channels_handler():
    return await get_channels()


@router.get(
    "/{channel_id}",
    response_model=BaseChannelResponse
)
async def get_channel_handler(channel_id: int):
    return await get_channel(pk=channel_id)


@router.delete(
    "/{channel_id}",
    response_model=BaseChannelResponse,
    responses={204: {"model": None}},
)
async def delete_channel_handler(channel_id: int):
    await delete_channel(pk=channel_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


__all__ = ('router',)
