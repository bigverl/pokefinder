from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.modules.candidate_finder.services import CandidateFinderService
from backend.src.lib.repository import SQLAlchemyRepository


async def provide_candidate_finder(db_session: AsyncSession) -> CandidateFinderService:
    repo = await SQLAlchemyRepository.create(session=db_session)
    return CandidateFinderService(repository=repo)