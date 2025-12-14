import pytest
import pytest_asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from backend.src.config.settings import settings
from litestar.plugins.sqlalchemy import UUIDBase
from scripts.seed_database import seed_database

# ==================
# Test Mode Setup
# ==================
@pytest.fixture(scope="session", autouse=True)
def setup_test_mode(request):
    if request.config.getoption("-m") == "unit":
        os.environ["TEST_MODE"] = "unit"
    else:
        os.environ["TEST_MODE"] = "integration"
    yield
    os.environ.pop("TEST_MODE", None)

@pytest_asyncio.fixture(scope="session")
async def seed_db_engine():
    """Create engine just to seed the database, then fully dispose"""
    engine = create_async_engine(settings.db_url, echo=False)
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)

    # seed database
    async with async_session_maker() as session:
        await seed_database(session)

    # dispose
    await engine.dispose()

    yield

# engine created once and used for all tests
@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def _db_engine(setup_test_mode):
    """Create engine and seed database once per test session"""
    engine = create_async_engine(settings.db_url, echo=False)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)

    # Create session maker
    async_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # Seed the database once per test session
    async with async_session_maker() as session:
        print(f"\n🌱 Seeding {settings.db_url.split('://')[0]} database for tests...")
        await seed_database(session)
        print("✅ Database seeded successfully\n")

    yield async_session_maker

    await engine.dispose()

# db session used only for tests
@pytest_asyncio.fixture
async def db_session():
    """Provide a fresh database session per test"""
    engine = create_async_engine(settings.db_url, echo=False)
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session_maker() as session:
        yield session

    await engine.dispose()
