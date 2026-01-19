import pytest_asyncio
from litestar.testing import AsyncTestClient
from backend.src.modules.candidate_finder.services import CandidateFinderService
from backend.src.lib.repository import SQLAlchemyRepository
from litestar import Litestar
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.modules.candidate_finder.controllers import CandidateFinderController

@pytest_asyncio.fixture(scope="session")
async def db_session_postgres(_db_engine_postgres):
    """Session-scoped database session for PostgreSQL"""
    async with _db_engine_postgres() as session:
        yield session

@pytest_asyncio.fixture(scope="session")
async def sqlalchemy_repo_postgres(db_session_postgres) -> SQLAlchemyRepository:
    return await SQLAlchemyRepository.create(session=db_session_postgres)

@pytest_asyncio.fixture(scope="session")
async def finder_postgres(sqlalchemy_repo_postgres) -> CandidateFinderService:
    """Session-scoped CandidateFinderService with PostgreSQL"""
    return CandidateFinderService(sqlalchemy_repo_postgres)
