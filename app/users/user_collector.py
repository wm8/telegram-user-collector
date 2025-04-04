from typing import Any

import telethon.tl.types
from telethon import TelegramClient
from telethon.tl.functions.contacts import GetContactsRequest, ImportContactsRequest, DeleteContactsRequest
from telethon.tl.functions.users import GetUsersRequest, GetFullUserRequest
from telethon.tl.types import InputUser, InputPhoneContact

from app.db.models import User
from app.telegram_client import telegram_api


def convert_to_user_model(response) -> User| None:
    if not response:
        return None
    if isinstance(response, telethon.tl.types.User):
        return User(**{
            'id': response.id,
            'username': response.username,
            'phone': response.phone
        })
    return User(**{
        'id': response.id,
    })

async def get_user_by_username(username: str)  -> User| None:
    client = await telegram_api.get_client()
    try:
        user = await client.get_entity(username)
        return convert_to_user_model(user)
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None

async def get_user_by_id(user_id: int) -> User| None:
    client = await telegram_api.get_client()
    try:
        user = InputUser(user_id=user_id, access_hash=0)  # access_hash можно оставить 0, если неизвестен
        result = await client(GetUsersRequest(id=[user]))
        if result and len(result) > 0:
            return convert_to_user_model(result[0])
        return None
    except Exception as e:
        print(f"Error fetching user by ID: {e}")
        return None


async def get_users_by_id(uids: list[id]) -> list[User]:
    client = await telegram_api.get_client()
    try:
        users = [InputUser(user_id=uid, access_hash=0) for uid in uids]
        result = await client(GetUsersRequest(id=users))
        return [convert_to_user_model(user_data) for user_data in result]
    except Exception as e:
        print(f"Error fetching user by ID: {e}")
        return []



async def get_full_user_by_id(user_id: int) -> User| None:
    client = await telegram_api.get_client()
    try:
        user = await client.get_entity(user_id)  # access_hash можно оставить 0, если неизвестен
        result = await client(GetFullUserRequest(user))
        if result:
            return convert_to_user_model(result.users[0])
        return None
    except Exception as e:
        print(f"Error fetching user by ID: {e}")
        return None


async def get_user_by_phone(phone_number: str) -> User| None:
    client = await telegram_api.get_client()
    try:
        contact = InputPhoneContact(
            client_id=0,
            phone=phone_number,
            first_name="Temp",
            last_name="User"
        )
        result = await client(ImportContactsRequest(contacts=[contact]))
        if result.users:
            user = result.users[0]
            await client(DeleteContactsRequest(id=[user]))
            return convert_to_user_model(user)
        else:
            return None
    except Exception as e:
        print(f"Error fetching user by phone: {e}")
        return None


