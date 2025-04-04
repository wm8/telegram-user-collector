from telethon import TelegramClient, events

from app.config.config import settings


class TelegramAPI:
    def __init__(self):
        self.client = TelegramClient(
            'session',
            settings.API_ID,
            settings.API_HASH
        )

        #self.client.start(bot_token=settings.BOT_TOKEN)

    async def init(self):
        await self.client.start()

    async def get_client(self):
        await self.client.connect()
        return self.client


telegram_api = TelegramAPI()