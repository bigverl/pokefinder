import pytest

from backend.src.lib.repository import JSONRepository
from backend.src.modules.candidate_finder.services import CandidateFinderService
from backend.src.modules.coverage_analyzer.services import CoverageAnalyzerService
from tests.unit.fixtures.fake_data import (
    MACHINE_MOVES_INDEX,
    MOVE_INDEX,
    MY_TEAM_STRENGTHS_TYPE_INDEX,
    OPPONENT_WEAKNESS_TYPE_INDEX,
    POKEMON_INDEX,
    STAT_INDEX,
    STAT_SPREAD_INDEX,
    TYPE_INDEX,
    TYPE_PAIRS,
)


@pytest.fixture(scope="session")
def fake_repo() -> JSONRepository:
    repo = JSONRepository.__new__(JSONRepository)
    repo.type_pairs = TYPE_PAIRS
    repo._pokemon_index = POKEMON_INDEX
    repo._move_index = MOVE_INDEX
    repo._stat_index = STAT_INDEX
    repo._stat_spread_index = STAT_SPREAD_INDEX
    repo._type_index = TYPE_INDEX
    repo._opponent_weakness_type_index = OPPONENT_WEAKNESS_TYPE_INDEX
    repo._my_team_strengths_type_index = MY_TEAM_STRENGTHS_TYPE_INDEX
    repo._machine_moves_index = MACHINE_MOVES_INDEX
    return repo


@pytest.fixture(scope="session")
def finder(fake_repo: JSONRepository) -> CandidateFinderService:
    return CandidateFinderService(fake_repo)


@pytest.fixture(scope="session")
def coverage_analyzer(fake_repo: JSONRepository) -> CoverageAnalyzerService:
    return CoverageAnalyzerService(fake_repo)
