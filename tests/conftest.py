import pytest
import pytest_asyncio
from backend.candidate_finder.services import CandidateFinder
from backend.candidate_finder.repository import (
    JsonRepository,
    SQLiteRepository
)
from tests.mock_repository import MockPokemonRepository
from config import (
    DATA_CACHE_DIR,
    SQLITE_DB_PATH
)

# ==================
# test_candidate_finder.py
# ===================
@pytest.fixture
def mock_repo() -> MockPokemonRepository:
    return MockPokemonRepository()

@pytest.fixture
def finder(mock_repo) -> CandidateFinder:
    return CandidateFinder(mock_repo)


# =====================
# test_json_repository.py
# ====================
@pytest.fixture
def json_repo() -> JsonRepository:
    return JsonRepository(data_dir=DATA_CACHE_DIR)


# =====================
# test_sqlite_repository.py
# ====================
@pytest_asyncio.fixture
async def sqlite_repo() -> SQLiteRepository:
    return await SQLiteRepository.create(db_path=SQLITE_DB_PATH)
