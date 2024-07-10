from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import DateTime
from datetime import datetime

from tgbot.config import DB_HOST, DB_NAME, DB_PASS, DB_USER, DB_PORT


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(
        DateTime(), default=datetime.now())
    updated: Mapped[DateTime] = mapped_column(
        DateTime(), default=datetime.now(), onupdate=datetime.now())


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def async_connect_to_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
