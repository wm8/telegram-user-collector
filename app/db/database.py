from contextlib import asynccontextmanager

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config.config import settings
from app.db.models import Base

# Создаем асинхронный движок
engine = create_async_engine(
    settings.DB_URL,  # Пример: postgresql+asyncpg://user:password@localhost/dbname
    echo=True  # Логирование SQL-запросов
)

# Создаем фабрику сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def create_table_async() -> None:
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def save_data(data: Base) -> bool:
    if not data:
        return False

    async with get_session() as session:
        session.add(data)
        await session.commit()
        return True

def to_dict(data: Base) -> dict:
    result = data.__dict__
    if '_sa_instance_state' in result:
        del result['_sa_instance_state']
    return result

async def insert_value(data: Base) -> bool:
    if not data:
        return False
    model_type = type(data)
    async with get_session() as session:
        query = insert(model_type).values([to_dict(data)]).on_conflict_do_nothing()
        await session.execute(query)
        await session.commit()

async def insert_data_collection(data: list[Base]):
    if len(data) == 0:
        return
    model_type = type(data[0])
    async with get_session() as session:
        query = insert(model_type).values([to_dict(x) for x in data]).on_conflict_do_nothing()
        await session.execute(query)
        await session.commit()

async def save_data_collection(data_collection: list[Base]):
    async with get_session() as session:
        for data in data_collection:
            session.add(data)
        await session.commit()
#
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session
#
# # Функция для получения сессии напрямую
# async def get_session():
#     async for session in get_db():
#         return session
#
# async def save_data(data: Base) -> bool:
#     session = await get_session()
#     async with session:
#         if not data:
#             return False
#         session.add(data)
#         await session.commit()
#         return True
#
# async def save_data_collection(data_collection: list[Base]):
#     session = await get_session()
#     async with session:
#         for data in data_collection:
#             session.add(data)
#         await session.commit()