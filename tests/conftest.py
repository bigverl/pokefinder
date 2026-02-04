import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from backend.src.config.settings import settings
from advanced_alchemy.base import UUIDBase
from scripts.seed_db import seed_database
from sqlalchemy.pool import StaticPool

# ==================
# SQLite Session-Scoped Setup (fast, shared across tests)
# ==================
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

    # Create tables + seed
    async with engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)
    async with async_session_maker() as session:
        await seed_database(session)

    yield async_session_maker
    await engine.dispose()

# ==================
# PostgreSQL Session-Scoped Setup (seeds once, shared across tests)
# ==================
@pytest_asyncio.fixture(scope="session")
async def _db_engine_postgres():
    """Session-scoped engine for PostgreSQL (seeds once, shared across tests)"""
    database_url = settings.database_url
    engine = create_async_engine(database_url, echo=False)

    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Create tables + seed once
    async with engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.drop_all)
        await conn.run_sync(UUIDBase.metadata.create_all)
    async with async_session_maker() as session:
        await seed_database(session)

    yield async_session_maker

    # Cleanup at end of session
    async with engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.drop_all)
    await engine.dispose()