import asyncio

import app.telegram_client as tg
from fastapi import FastAPI, HTTPException

from app.channel.channel_info_collector import get_channel_info_by_username
from app.channel.channel_message_collector import get_channel_messages, parse_full_channel, parse_channel_users
from app.db.database import save_data, insert_data_collection, insert_value
from app.db.models import User, Channel, Message
from app.telegram_client import telegram_api
from app.users.user_collector import get_user_by_username, get_user_by_id, get_user_by_phone, get_full_user_by_id

asyncio.run(telegram_api.init())
# Создаем экземпляр приложения FastAPI
app = FastAPI()

@app.get("/users/{username}")
async def get_user(username: str):
    """
    Вернуть данные по пользователю по username
    """
    user : User = await get_user_by_username(username)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")

    return user

@app.get("/users/save/{username}")
async def save_user(username: str):
    """
    Сохранить информацию о пользователе с username в базе данных
    """
    user : User = await get_user_by_username(username)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    await save_data(user)
    return user

@app.get("/users/by_id/{id}")
async def get_user_by_id_route(uid: int):
    """
    Вернуть данные по пользователю по id
    """
    user : User = await get_full_user_by_id(uid)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")

    return user



@app.get("/channels/{username}")
async def get_channel(username: str):
    """
    Вернуть данные по канала по username
    """
    channel : Channel = await get_channel_info_by_username(username)

    if not channel:
        raise HTTPException(status_code=404, detail="Канал не найден!")

    return channel

@app.get("/channels/get_messages_by_username/{username}")
async def get_channel_messages_route(username: str):
    """
    Вернуть данные по канала по username
    """
    channel : Channel = await get_channel_info_by_username(username)
    await insert_value(channel)

    messages : list[Message] = await get_channel_messages(username)

    if len(messages) == 0:
        raise HTTPException(status_code=404, detail="Канал не найден!")

    await insert_data_collection(messages)

    return messages

@app.get("/channels/get_full_info/{username}")
async def get_full_info_route(username: str):
    """
    Вернуть данные по канала по username
    """
    channel, messages, comments = await parse_full_channel(username)
    if not channel:
        raise HTTPException(status_code=404, detail="Канал не найден!")
    await insert_value(channel)
    await insert_data_collection(messages)
    await insert_data_collection(comments)
    return messages

@app.get("/channels/get_users/{username}")
async def get_full_info_route(username: str):
    """
    Вернуть данные по канала по username
    """
    users : set[User] = await parse_channel_users(username)
    if not users:
        raise HTTPException(status_code=404, detail="Канал не найден!")
    await insert_data_collection(list(users))
    return list(users)