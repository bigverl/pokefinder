import pytest_asyncio
from advanced_alchemy.base import UUIDBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from scripts.seed_db import seed_database


@pytest_asyncio.fixture(scope="session")
async def _db_engine():
    """Session-scoped engine for SQLite (fast, shared across tests)"""
    database_url = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)
    async with async_session_maker() as session:
        await seed_database(session)

    yield async_session_maker
    await engine.dispose()
