import asyncio

from app.channel.channel_message_collector import get_users_from_channel, parse_channel_users
from app.telegram_client import telegram_api
import sys

async def main():
    if len(sys.argv) < 2:
        print("Usage: main.py <channel-name>")
        return
    channel_name = sys.argv[1]
    await telegram_api.init()
    await parse_channel_users(channel_name)


if __name__ == "__main__":
    asyncio.run(main())