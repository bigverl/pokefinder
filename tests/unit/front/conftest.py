import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.src.modules.candidate_finder.schemas import (
    CandidateFinderResponse,
    MovesTable,
    MovesTableRow,
    StatsTable,
    StatsTableRow,
    TypesTable,
    TypesTableRow,
)


@pytest.fixture
def mock_api_response():
    """Sample CandidateFinderResponse for testing."""
    return CandidateFinderResponse(
        moves_table=MovesTable(rows=[
            MovesTableRow(
                pokemon_name="pikachu",
                move_name="thunderbolt",
                level_learned=26,
                machine="TM24",
                egg_move=None
            ),
            MovesTableRow(
                pokemon_name="raichu",
                move_name="thunderbolt",
                level_learned=1,
                machine="TM24",
                egg_move=None
            ),
        ]),
        stats_table=StatsTable(rows=[
            StatsTableRow(
                name="pikachu",
                attack=55,
                defense=40,
                special_attack=50,
                special_defense=50,
                speed=90
            ),
            StatsTableRow(
                name="raichu",
                attack=90,
                defense=55,
                special_attack=90,
                special_defense=80,
                speed=110
            ),
        ]),
        types_table=TypesTable(rows=[
            TypesTableRow(name="pikachu", type1="electric", type2=None),
            TypesTableRow(name="raichu", type1="electric", type2=None),
        ])
    )


@pytest.fixture
def mock_backend_client(mock_api_response):
    """Mock BackendClient that returns sample data."""
    client = AsyncMock()
    client.search_pokemon = AsyncMock(return_value=mock_api_response)
    client.close = AsyncMock()
    return client
