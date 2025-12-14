import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from backend.src.config.settings import settings
from advanced_alchemy.base import UUIDBase
from scripts.seed_database import seed_database
from sqlalchemy.pool import StaticPool

# ==================
# SQLite Session-Scoped Setup (fast, shared across tests)
# ==================
@pytest_asyncio.fixture(scope="session")
async def _db_engine():
    """Session-scoped engine for SQLite (fast, shared across tests)"""
    db_url = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(
        db_url,
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
# PostgreSQL Function-Scoped Setup (slower, but avoids concurrent operation errors)
# ==================
@pytest_asyncio.fixture(scope="function")
async def _db_engine_postgres():
    """Function-scoped engine for PostgreSQL (creates fresh DB per test)"""
    db_url = settings.db_url
    engine = create_async_engine(db_url, echo=False)

    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Create tables + seed for each test
    async with engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)
    async with async_session_maker() as session:
        await seed_database(session)

    yield async_session_maker

    # Cleanup: drop all tables after each test
    async with engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.drop_all)
    await engine.dispose()