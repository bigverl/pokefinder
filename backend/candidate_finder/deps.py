from config import (
    SQLITE_DB_PATH
)
from litestar.datastructures import State
from backend.candidate_finder.services import CandidateFinder
from backend.candidate_finder.repository import SQLiteRepository

async def provide_sqlite_candidate_finder(state: State) -> CandidateFinder:
    # Provide a CandidateFinder with SQLite backend
    repository = await SQLiteRepository(SQLITE_DB_PATH).create()

    return CandidateFinder(repository)