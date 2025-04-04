import asyncio

import telethon
from telethon.errors import MessageIdInvalidError
from tqdm import tqdm

from app.channel.channel_info_collector import convert_to_channel_model, get_channel_info_by_username
from app.db.models import Message, Comment, User
from telethon.tl.types import Channel
from app.telegram_client import telegram_api
from app.users.user_collector import convert_to_user_model


def convert_to_message_model(message: telethon.tl.types.Message) -> Message | None:
    if not message:
        return None
    return Message(**{
        'mid': message.id,
        'date': message.date,
        'text': message.message,
        'channel_id': message.chat_id
    })

def convert_to_comment_model(message: telethon.tl.types.Message) -> Comment | None:
    if not message or not message.message:
        return None
    return Comment(**{
        'mid': message.id,
        'date': message.date,
        'text': message.message,
        'channel_id': message.chat_id
    })

async def get_channel_messages(channel_username) -> list[Message]:
    client = await telegram_api.get_client()
    channel = await client.get_entity(channel_username)
    messages = []
    i=0
    async for message in client.iter_messages(channel):
        if i > 500:
            i=0
            await asyncio.sleep(0.5)
        i += 1
        if not message.message:
            continue
        message: Message = convert_to_message_model(message)
        if message:
            messages.append(message)
    return messages

async def get_message_comments(message: Message) -> list[Comment]:
    client = await telegram_api.get_client()
    comments = []
    # Проверяем, что канал поддерживает комментарии
    # if not isinstance(message.chat, Channel):
    #     print("Это не канал или группа, комментарии недоступны.")
    #     return comments

    try:
        i = 0
        async for com_data in client.iter_messages(
                message.channel_id,  # Используем chat вместо channel_id
                reply_to=message.mid,  # Используем id вместо mid
                limit=100
        ):
            if i > 500:
                i = 0
                await asyncio.sleep(0.5)  # Задержка для соблюдения лимитов API
            i += 1
            if isinstance(com_data.sender, Channel):
                continue
            # Преобразуем данные в модель Comment
            comment = convert_to_comment_model(com_data)
            if comment:
                comments.append(comment)
    except MessageIdInvalidError:
        print(f"Ошибка: Некорректный ID сообщения {message.id}.")
    except Exception as e:
        print(f"Ошибка при получении комментариев: {e}")

    return comments


async def get_message_comments_raw(message: Message) -> list[telethon.tl.types.Message]:
    client = await telegram_api.get_client()
    comments = []

    try:
        async for comment in client.iter_messages(
                message.channel_id,  # Используем chat вместо channel_id
                reply_to=message.mid,  # Используем id вместо mid
                limit=100
        ):
            if comment:
                comments.append(comment)
    except MessageIdInvalidError:
        print(f"Ошибка: Некорректный ID сообщения {message.id}.")
    except Exception as e:
        print(f"Ошибка при получении комментариев: {e}")

    return comments


async def parse_full_channel(channel_username: str) -> (Channel, list[Message], list[Comment]):
    channel = await get_channel_info_by_username(channel_username)
    if not channel:
        return None, None, None
    print('Collecting messages from channel')
    messages = await get_channel_messages(channel.username)
    if not messages or len(messages) < 1:
        return channel, [], []
    comments = []

    for message in tqdm(messages, desc='Collecting message comments'):
        comments.extend(await get_message_comments(message))
    return channel, messages, comments

async def parse_channel_users(channel_username: str) -> set[User]:
    channel = await get_channel_info_by_username(channel_username)
    if not channel:
        return None
    print('Collecting messages from channel')
    messages = await get_channel_messages(channel.username)
    if not messages or len(messages) < 1:
        return set()
    users = set()

    for message in tqdm(messages, desc='Collecting message comments'):
        comments = [x for x in await get_message_comments_raw(message) if x and not isinstance(x.sender, Channel)]
        new_users = [ y for y in [convert_to_user_model(x.sender) for x in comments] if y is not None ]
        users.update(new_users)
    return users


async def get_users_from_channel(channel_username: str) -> set[User]:
    client = await telegram_api.get_client()
    channel = await client.get_entity(channel_username)
    users = set()
    i = 0
    async for mess_data in client.iter_messages(channel):
        if i > 500:
            i = 0
            await asyncio.sleep(0.5)
        i += 1
        message = convert_to_message_model(mess_data)
        comments = [ x for x in await get_message_comments_raw(message) if x and not isinstance(x.sender, Channel)]
        users.update([convert_to_user_model(x.sender) for x in comments])
    return users



