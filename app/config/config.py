import os
from dotenv import load_dotenv
#from pydantic import BaseSettings

load_dotenv()

class Settings():
    API_ID: int = os.getenv("API_ID")
    API_HASH: str = os.getenv("API_HASH")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    DB_URL: str = os.getenv("DB_URL", "postgresql+psycopg://postgres:123@localhost:5432/postgres")

settings = Settings()