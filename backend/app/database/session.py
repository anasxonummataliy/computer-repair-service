from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings

async_engine = create_async_engine(settings.db_url, future=True)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session


@asynccontextmanager
async def async_session() -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session