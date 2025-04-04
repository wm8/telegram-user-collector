from telethon.tl.functions.channels import GetFullChannelRequest

from app.db.models import Channel
from app.telegram_client import telegram_api


def convert_to_channel_model(response) -> Channel | None:
    if response is None:
        return None
    def_chat_info = response.chats[0]
    full_chat = response.full_chat
    return Channel(**{
        'id': -full_chat.id + -1000000000000,
        "username": def_chat_info.username,
        'title': def_chat_info.title,
        'description': full_chat.about,
        'subscriptions' : full_chat.participants_count
    })

async def get_channel_info_by_username(channel_identifier):
    client = await telegram_api.get_client()
    try:
        channel = await client.get_entity(channel_identifier)
        full_info = await client(GetFullChannelRequest(channel))
        return convert_to_channel_model(full_info)
    except Exception as e:
        print(f"Channel error: {e}")
        return None