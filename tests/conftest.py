import pytest
import pytest_asyncio
import os
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
# Test Mode Setup
# ==================
@pytest.fixture(scope="session", autouse=True)
def setup_test_mode(request):
    """Set TEST_MODE based on test file location"""
    test_path = str(request.fspath)

    if "/tests/unit/" in test_path or "/zzz_4.5_testing/" in test_path:
        os.environ["TEST_MODE"] = "unit"
    elif "/tests/integration/" in test_path:
        os.environ["TEST_MODE"] = "integration"

    yield

    os.environ.pop("TEST_MODE", None)

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
