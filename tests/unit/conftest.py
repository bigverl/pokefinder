import pytest
import pytest_asyncio
from backend.src.modules.candidate_finder.services import CandidateFinderService
from backend.src.lib.repository import SQLAlchemyRepository
from tests.unit.mock_repository import MockRepository

# ==================
# test_candidate_finder.py
# ===================
@pytest.fixture
def mock_repo() -> MockRepository:
    return MockRepository()

@pytest_asyncio.fixture
async def finder(sqlalchemy_repo) -> CandidateFinderService:
    """Create CandidateFinderService with the seeded repository (SQLite)"""
    return CandidateFinderService(sqlalchemy_repo)

@pytest_asyncio.fixture
async def finder_postgres(sqlalchemy_repo_postgres) -> CandidateFinderService:
    """Create CandidateFinderService with the seeded repository (PostgreSQL - function-scoped)"""
    return CandidateFinderService(sqlalchemy_repo_postgres)

# =====================
# test_sqlalchemy_repository.py
# ====================
@pytest_asyncio.fixture
async def db_session(_db_engine):
    """Create a new database session for each test (SQLite - session-scoped)"""
    async with _db_engine() as session:
        yield session

@pytest_asyncio.fixture
async def db_session_postgres(_db_engine_postgres):
    """Create a new database session for each test (PostgreSQL - function-scoped)"""
    async with _db_engine_postgres() as session:
        yield session

@pytest_asyncio.fixture
async def sqlalchemy_repo(db_session) -> SQLAlchemyRepository :
    return await SQLAlchemyRepository.create(session=db_session)

@pytest_asyncio.fixture
async def sqlalchemy_repo_postgres(db_session_postgres) -> SQLAlchemyRepository :
    return await SQLAlchemyRepository.create(session=db_session_postgres)


