import pytest
import pytest_asyncio
from litestar import Litestar
from litestar.di import Provide
from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.lib.repository import SQLAlchemyRepository
from backend.src.modules.candidate_finder.controllers import CandidateFinderController
from backend.src.modules.candidate_finder.services import CandidateFinderService
from backend.src.modules.coverage_analyzer.controllers import CoverageAnalyzerController
from backend.src.modules.coverage_analyzer.services import CoverageAnalyzerService


@pytest.fixture(scope="session")
async def test_app(_db_engine):
    """Create a test Litestar app using the SQLite test database."""

    async def provide_test_finder(db_session: AsyncSession):
        repo = await SQLAlchemyRepository.create(session=db_session)
        return CandidateFinderService(repository=repo)

    async def provide_test_coverage_analyzer(db_session: AsyncSession):
        repo = await SQLAlchemyRepository.create(session=db_session)
        return CoverageAnalyzerService(repository=repo)

    async def provide_test_session():
        async with _db_engine() as session:
            yield session

    app = Litestar(
        route_handlers=[CandidateFinderController, CoverageAnalyzerController],
        dependencies={
            "db_session": Provide(provide_test_session),
            "finder": Provide(provide_test_finder),
            "coverage_analyzer": Provide(provide_test_coverage_analyzer),
        },
        debug=True,
    )
    return app


@pytest.fixture(scope="session")
def test_client(test_app):
    """Create a TestClient for the test app."""
    with TestClient(app=test_app) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def db_session(_db_engine):
    """Create a new database session for each test (SQLite - session-scoped)"""
    async with _db_engine() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def sqlalchemy_repo(db_session: AsyncSession) -> SQLAlchemyRepository:
    return await SQLAlchemyRepository.create(session=db_session)
