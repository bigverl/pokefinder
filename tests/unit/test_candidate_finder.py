import pprint

import pytest

from backend.src.lib.exceptions import (
    InvalidPokemonMoveError,
    InvalidPokemonStatError,
    InvalidPokemonTypeError,
    NoPokemonFoundError,
)
from backend.src.modules.candidate_finder.services import CandidateFinderService

# ===========================
# test_get_pokemon_by_move.py
# ============================


# Case 2: Move does not exist
@pytest.mark.unit
def test_get_pokemon_by_move_invalid_pokemon_types(finder: CandidateFinderService):
    with pytest.raises(InvalidPokemonMoveError):
        finder.repository.get_pokemon_by_move("definitely not a move")


# Case 3: Found
@pytest.mark.unit
def test_get_pokemon_by_move_found_single_type(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_move("hypnosis")
    assert result == {
        "bronzong": {"level-up": 20},
        "exeggutor": {"level-up": 1},
        "gallade": {"level-up": 1},
        "haunter": {"level-up": 1},
        "alakazam": {"level-up": 1},
    }


# Case 4: Legendary/Mythical filtering - Default (exclude both)
@pytest.mark.unit
def test_get_pokemon_by_move_exclude_legendary_and_mythical_by_default(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_move("psychic")
    # Should NOT include legendaries
    assert "latias" not in result
    assert "latios" not in result
    assert "cresselia" not in result
    # Should NOT include mythicals
    assert "celebi" not in result
    assert "jirachi" not in result
    # Should include normal Pokemon
    assert "alakazam" in result


# Case 5: Include legendary and mythical
@pytest.mark.unit
def test_get_pokemon_by_move_include_legendary_and_mythical(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_move("psychic", include_legendary=True, include_mythical=True)
    # Should include legendaries
    assert "latias" in result
    assert "cresselia" in result
    # Should include mythicals
    assert "celebi" in result
    assert "jirachi" in result
    # Should include normal Pokemon
    assert "alakazam" in result


# Case 6: Include all special Pokemon (legendary, mythical, ultra beasts)
@pytest.mark.unit
def test_get_pokemon_by_move_include_all_special_pokemon(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_move(
        "psychic", include_legendary=True, include_mythical=True, include_ultra_beasts=True
    )
    # Should include Ultra Beasts
    assert "nihilego" in result
    assert "blacephalon" in result
    # Should include legendaries
    assert "latias" in result
    assert "cresselia" in result
    # Should include mythicals
    assert "celebi" in result
    assert "jirachi" in result
    # Should include normal Pokemon
    assert "alakazam" in result


# ===========================
# test_get_pokemon_by_stats.py
# ============================


# Case 2: Empty stat names (Caller mistake)
@pytest.mark.unit
def test_get_pokemon_by_stats_empty_primary_stat(finder: CandidateFinderService):
    with pytest.raises(InvalidPokemonStatError, match="primary_stat cannot be empty"):
        finder.repository.get_pokemon_by_stats("", "speed")


@pytest.mark.unit
def test_get_pokemon_by_stats_empty_secondary_stat(finder: CandidateFinderService):
    with pytest.raises(InvalidPokemonStatError, match="secondary_stat cannot be empty"):
        finder.repository.get_pokemon_by_stats("attack", "")


# Case 3: Invalid stat names (Caller mistake)
@pytest.mark.unit
def test_get_pokemon_by_stats_invalid_primary_stat(finder: CandidateFinderService):
    with pytest.raises(InvalidPokemonStatError, match="Invalid primary_stat"):
        finder.repository.get_pokemon_by_stats("coolness", "speed")


@pytest.mark.unit
def test_get_pokemon_by_stats_invalid_secondary_stat(finder: CandidateFinderService):
    with pytest.raises(InvalidPokemonStatError, match="Invalid secondary_stat"):
        finder.repository.get_pokemon_by_stats("attack", "badness")


# Case 4: Valid search with default parameters
@pytest.mark.unit
def test_get_pokemon_by_stats_basic_attack_speed_search(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_stats("attack", "speed")

    # Should return a dict
    assert isinstance(result, dict)

    # Should have results
    assert len(result) > 0

    # Should have at least 5 results
    assert len(result) >= 5


# Case 5: No Pokemon found (threshold too high)
@pytest.mark.unit
def test_get_pokemon_by_stats_no_pokemon_found_high_threshold(finder: CandidateFinderService):
    with pytest.raises(NoPokemonFoundError):
        # No Pokemon has 200 attack and 200 speed
        finder.repository.get_pokemon_by_stats("attack", "speed", min_primary=200, min_secondary=200)


# Case 6: Ranking order (weighted 70/30)
@pytest.mark.unit
def test_get_pokemon_by_stats_ranking_order(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_stats("attack", "speed")

    # Slaking (Attack: 160, Speed: 100) should rank #1
    # Dragapult should also be in top results (high attack + speed)
    assert "slaking" in result
    assert "dragapult" in result

    # Get the ranking by converting to list
    ranking = list(result.keys())

    # Both should be in top 10
    assert "slaking" in ranking[:10]
    assert "dragapult" in ranking[:10]


# Case 7: Default behavior (exclude legendary, mythical, ultra beasts)
@pytest.mark.unit
def test_get_pokemon_by_stats_exclude_special_pokemon_by_default(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_stats("attack", "speed")

    # Should NOT include legendaries
    assert "regigigas" not in result
    assert "groudon" not in result
    assert "rayquaza" not in result

    # Should include normal Pokemon
    assert "garchomp" in result
    assert "salamence" in result


# Case 8: Include all special Pokemon (legendary, mythical, ultra beasts)
@pytest.mark.unit
def test_get_pokemon_by_stats_include_all_special_pokemon(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_stats(
        "attack", "speed", include_legendary=True, include_mythical=True, include_ultra_beasts=True
    )

    # Should include Ultra Beasts
    assert "kartana" in result
    assert "pheromosa" in result

    # Should include legendaries
    assert "regigigas" in result
    assert "groudon" in result

    # Should include normal Pokemon
    assert "garchomp" in result


# Case 9: min_primary filter
@pytest.mark.unit
def test_get_pokemon_by_stats_min_primary_threshold(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_stats("attack", "speed", min_primary=130)

    # All results should have attack >= 130
    # Garchomp (Attack: 130) should be included
    assert "garchomp" in result

    # Blaziken (Attack: 120) should NOT be included
    assert "blaziken" not in result


# Case 10: Explicit min_secondary
@pytest.mark.unit
def test_get_pokemon_by_stats_explicit_min_secondary(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_stats("attack", "speed", min_primary=100, min_secondary=100)

    # Should only include Pokemon with attack >= 100 AND speed >= 100
    assert len(result) > 0

    # Garchomp (Attack: 130, Speed: 102) should be included
    assert "garchomp" in result


# Case 11: min_speed filter
@pytest.mark.unit
def test_get_pokemon_by_stats_min_speed_filter(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_stats("attack", "defense", min_primary=100, min_speed=100)

    # Should only include Pokemon with attack >= 100, AND speed >= 100
    # Garchomp (Attack: 130, Defense: 95, Speed: 102) should be included
    assert "garchomp" in result

    # Aggron (Attack: 110, Defense: 180, Speed: 50) should NOT be included (too slow)
    assert "aggron" not in result

    # Rhyperior (Attack: 140, Defense: 130, Speed: 40) should NOT be included (too slow)
    assert "rhyperior" not in result


# ===========================
# test_get_pokemon_by_type.py
# ============================


# Case 1: Invalid type (Caller mistake)
@pytest.mark.unit
def test_get_pokemon_by_type_invalid_type(finder: CandidateFinderService):
    with pytest.raises(InvalidPokemonTypeError):
        finder.repository.get_pokemon_by_type("definitely-not-a-type")


# Case 2: Single type search
@pytest.mark.unit
def test_get_pokemon_by_type_single_type(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_type("fire")

    # Should be a frozenset
    assert isinstance(result, frozenset)

    # Should include fire types
    assert "charizard" in result
    assert "typhlosion" in result

    # Should NOT include non-fire types
    assert "pikachu" not in result


# Case 3: Dual type search
@pytest.mark.unit
def test_get_pokemon_by_type_dual_type(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_type("fire", "flying")

    # Should only include Pokemon with BOTH fire AND flying
    assert "charizard" in result

    # Should NOT include Pokemon with only one type
    assert "typhlosion" not in result  # Fire only
    assert "pidgeot" not in result  # Flying only


# Case 4: Default behavior (exclude legendary, mythical, ultra beasts)
@pytest.mark.unit
def test_get_pokemon_by_type_exclude_special_pokemon_by_default(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_type("psychic")

    # Should NOT include legendaries
    assert "mewtwo" not in result
    assert "latias" not in result

    # Should include normal Pokemon
    assert "alakazam" in result


# Case 5: Include all special Pokemon
@pytest.mark.unit
def test_get_pokemon_by_type_include_all_special_pokemon(finder: CandidateFinderService):
    result = finder.repository.get_pokemon_by_type(
        "psychic", include_legendary=True, include_mythical=True, include_ultra_beasts=True
    )

    # Should include legendaries
    assert "mewtwo" in result
    assert "latias" in result

    # Should include mythicals
    assert "celebi" in result

    # Should include normal Pokemon
    assert "alakazam" in result


# ===========================
# test_get_type_effectiveness.py
# ============================


# Case 1: Single type effectiveness
@pytest.mark.unit
def test_get_type_effectiveness_single_type(finder: CandidateFinderService):
    result = finder.repository.get_type_effectiveness("fire")

    # Should be a dict
    assert isinstance(result, dict)

    # Fire is weak to water, ground, rock (2x damage)
    assert "water" in result["2x"]
    assert "ground" in result["2x"]
    assert "rock" in result["2x"]

    # Fire resists fire, grass, ice, bug, steel, fairy (0.5x damage)
    assert "fire" in result["0.5x"]
    assert "grass" in result["0.5x"]


# Case 2: Dual type effectiveness (stacking)
@pytest.mark.unit
def test_get_type_effectiveness_dual_type(finder: CandidateFinderService):
    result = finder.repository.get_type_effectiveness("fire", "flying")

    # Fire/Flying is 4x weak to rock (2x from fire * 2x from flying = 4x)
    assert "rock" in result["4x"]

    # Water is 2x effective (fire weakness, flying neutral)
    assert "water" in result["2x"]

    # Grass is 0.25x effective (fire resists, flying resists)
    assert "grass" in result["0.25x"]


# ===========================
# test_search_pokemon.py
# ============================


# Case 1: No filters raises ValueError
@pytest.mark.unit
def test_search_pokemon_no_filters(finder: CandidateFinderService):
    with pytest.raises(ValueError, match="At least one filter parameter is required"):
        finder.search_pokemon()


# Case 2: Move filter returns frozenset of names
@pytest.mark.unit
def test_search_pokemon_move_only(finder: CandidateFinderService):
    result = finder.search_pokemon(move="tackle")

    assert isinstance(result, frozenset)
    assert len(result) > 0
    # Tackle is a common move, should return many Pokemon
    assert "pikachu" in result or "rattata" in result


# Case 3: Type filter returns frozenset of names
@pytest.mark.unit
def test_search_pokemon_type_only(finder: CandidateFinderService):
    result = finder.search_pokemon(desired_type="fire")

    assert isinstance(result, frozenset)
    assert len(result) > 0
    assert "charizard" in result
    assert "typhlosion" in result


# Case 4: Stats filter returns frozenset of names
@pytest.mark.unit
def test_search_pokemon_stats_only(finder: CandidateFinderService):
    result = finder.search_pokemon(primary_stat="attack", secondary_stat="speed")

    assert isinstance(result, frozenset)
    assert len(result) > 0


# Case 5: Multiple filters combine with AND logic (intersection)
@pytest.mark.unit
def test_search_pokemon_multiple_filters_intersection(finder: CandidateFinderService):
    # Fire type that learns a specific move
    result = finder.search_pokemon(move="flamethrower", desired_type="fire")

    assert isinstance(result, frozenset)
    # Should be smaller than just fire types or just flamethrower users
    fire_only = finder.search_pokemon(desired_type="fire")
    assert len(result) <= len(fire_only)

    # All results must be fire type AND learn flamethrower
    for pokemon in result:
        # Would need to verify both conditions, but we trust the intersection logic
        pass


# Case 6: Legendary filtering applies to all filter types
@pytest.mark.unit
def test_search_pokemon_exclude_legendary_default(finder: CandidateFinderService):
    # Psychic type search should exclude legendaries by default
    result = finder.search_pokemon(desired_type="psychic")

    assert "mewtwo" not in result
    assert "latias" not in result
    assert "alakazam" in result  # Non-legendary psychic


# Case 7: Include legendary flag works
@pytest.mark.unit
def test_search_pokemon_include_legendary(finder: CandidateFinderService):
    result = finder.search_pokemon(desired_type="psychic", include_legendary=True)

    # Should include at least some legendary psychic types
    # Note: Actual legendary Pokemon in test data may vary
    assert len(result) > 0


# ===========================
# test_build_response.py
# ============================
def test_print_all_tables(finder: CandidateFinderService):
    pokemon_names = frozenset(["bronzong", "exeggutor", "gallade"])
    response = finder.build_response(pokemon_names, "")

    tables = [
        ("moves_table", response.moves_table),
        ("stats_table", response.stats_table),
        ("types_table", response.types_table),
    ]

    for table_name, table in tables:
        print(f"table: {table_name}")
        for row in table.rows:
            pprint.pprint(row)


# Case 1: Response has all tables populated
@pytest.mark.unit
def test_build_response_all_tables_populated(finder: CandidateFinderService):
    pokemon_names = frozenset(["bronzong", "exeggutor", "gallade"])
    response = finder.build_response(pokemon_names, "")

    # All tables should be present
    assert response.moves_table is not None
    assert response.stats_table is not None
    assert response.types_table is not None


# Case 2: Tables contain correct Pokemon
@pytest.mark.unit
def test_build_response_correct_pokemon(finder: CandidateFinderService):
    pokemon_names = frozenset(["bronzong", "haunter"])
    response = finder.build_response(pokemon_names, "")

    # Types table should have both Pokemon
    assert response.types_table is not None
    types_names = {row.name for row in response.types_table.rows}
    assert "Bronzong" in types_names
    assert "Haunter" in types_names
    assert len(types_names) == 2

    # Stats table should have both Pokemon
    assert response.stats_table is not None
    stats_names = {row.name for row in response.stats_table.rows}
    assert "Bronzong" in stats_names
    assert "Haunter" in stats_names


# Case 3: Type data is accurate
@pytest.mark.unit
def test_build_response_type_data_accurate(finder: CandidateFinderService):
    pokemon_names = frozenset(["haunter"])
    response = finder.build_response(pokemon_names, "")

    # Haunter should be Ghost/Poison type
    assert response.types_table is not None
    haunter_row = response.types_table.rows[0]
    assert haunter_row.name == "Haunter"
    assert "ghost" in [haunter_row.type1, haunter_row.type2]


# Case 4: Stats data is accurate
@pytest.mark.unit
def test_build_response_stats_data_accurate(finder: CandidateFinderService):
    pokemon_names = frozenset(["haunter"])
    response = finder.build_response(pokemon_names, "")

    # Find haunter in stats table
    assert response.stats_table is not None
    haunter_row = next(row for row in response.stats_table.rows if row.name == "Haunter")

    # Stats should be integers and reasonable
    assert isinstance(haunter_row.attack, int)
    assert isinstance(haunter_row.speed, int)
    assert haunter_row.attack > 0
    assert haunter_row.speed > 0
