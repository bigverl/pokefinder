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
    """Create CandidateFinderService with the seeded SQLite repository"""
    return CandidateFinderService(sqlalchemy_repo)

# =====================
# test_sqlalchemy_repository.py
# ====================
@pytest_asyncio.fixture
async def sqlalchemy_repo(db_session) -> SQLAlchemyRepository :
    return await SQLAlchemyRepository.create(session=db_session)

