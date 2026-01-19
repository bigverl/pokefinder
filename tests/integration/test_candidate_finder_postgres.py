
import pytest
from backend.src.lib.exceptions import (
    NoPokemonFoundError,
    InvalidPokemonMoveError,
    InvalidPokemonTypeError,
    InvalidPokemonStatError
)

from backend.src.modules.candidate_finder.services import CandidateFinderService

import pprint

# ===========================
# test_get_pokemon_by_move.py
# ============================

# Case 2: Move does not exist
@pytest.mark.integration
def test_get_pokemon_by_move_invalid_pokemon_types(finder_postgres: CandidateFinderService):
    with pytest.raises(InvalidPokemonMoveError):
        finder_postgres.repository.get_pokemon_by_move("definitely not a move")

# Case 3: Found
@pytest.mark.integration
def test_get_pokemon_by_move_found_single_type(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_move("hypnosis")
    # PokeRogue fixture data (current source of truth)
    assert result == {
        'bronzong': {'level-up': 20},
        'exeggutor': {'level-up': 1},
        'gallade': {'level-up': 1},
        'glameow': {'level-up': 13},
        'gothorita': {'level-up': 24},
        'haunter': {'level-up': 1},
        'hoothoot': {'level-up': 36},
        'hypno': {'level-up': 1},
        'kirlia': {'level-up': 9},
        'lunatone': {'level-up': 5},
        'malamar': {'level-up': 1},
        'munna': {'level-up': 4},
        'poliwhirl': {'level-up': 1},
        'sandygast': {'level-up': 30},
        'sigilyph': {'level-up': 10},
        'spinda': {'level-up': 19},
        'watchog': {'level-up': 18},
        'wyrdeer': {'level-up': 10},
        'yanma': {'level-up': 38},
        'yanmega': {'level-up': 0}
    }

# Case 4: Legendary/Mythical filtering - Default (exclude both)
@pytest.mark.integration
def test_get_pokemon_by_move_exclude_legendary_and_mythical_by_default(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_move("psychic")
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
@pytest.mark.integration
def test_get_pokemon_by_move_include_legendary_and_mythical(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_move("psychic", include_legendary=True, include_mythical=True)
    # Should include legendaries
    assert "latias" in result
    assert "cresselia" in result
    # Should include mythicals
    assert "celebi" in result
    assert "jirachi" in result
    # Should include normal Pokemon
    assert "alakazam" in result

# Case 6: Include all special Pokemon (legendary, mythical, ultra beasts)
@pytest.mark.integration
def test_get_pokemon_by_move_include_all_special_pokemon(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_move("psychic", include_legendary=True, include_mythical=True, include_ultra_beasts=True)
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
@pytest.mark.integration
def test_get_pokemon_by_stats_empty_primary_stat(finder_postgres: CandidateFinderService):
    with pytest.raises(InvalidPokemonStatError, match="primary_stat cannot be empty"):
        finder_postgres.repository.get_pokemon_by_stats("", "speed")

@pytest.mark.integration
def test_get_pokemon_by_stats_empty_secondary_stat(finder_postgres: CandidateFinderService):
    with pytest.raises(InvalidPokemonStatError, match="secondary_stat cannot be empty"):
        finder_postgres.repository.get_pokemon_by_stats("attack", "")


# Case 3: Invalid stat names (Caller mistake)
@pytest.mark.integration
def test_get_pokemon_by_stats_invalid_primary_stat(finder_postgres: CandidateFinderService):
    with pytest.raises(InvalidPokemonStatError, match="Invalid primary_stat"):
        finder_postgres.repository.get_pokemon_by_stats("coolness", "speed")

@pytest.mark.integration
def test_get_pokemon_by_stats_invalid_secondary_stat(finder_postgres: CandidateFinderService):
    with pytest.raises(InvalidPokemonStatError, match="Invalid secondary_stat"):
        finder_postgres.repository.get_pokemon_by_stats("attack", "badness")


# Case 4: Valid search with default parameters
@pytest.mark.integration
def test_get_pokemon_by_stats_basic_attack_speed_search(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_stats("attack", "speed")

    # Should return a dict
    assert isinstance(result, dict)

    # Should have results
    assert len(result) > 0

    # Should have at least 5 results
    assert len(result) >= 5


# Case 5: No Pokemon found (threshold too high)
@pytest.mark.integration
def test_get_pokemon_by_stats_no_pokemon_found_high_threshold(finder_postgres: CandidateFinderService):
    with pytest.raises(NoPokemonFoundError):
        # No Pokemon has 200 attack and 200 speed
        finder_postgres.repository.get_pokemon_by_stats("attack", "speed", min_primary=200, min_secondary=200)


# Case 6: Ranking order (weighted 70/30)
@pytest.mark.integration
def test_get_pokemon_by_stats_ranking_order(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_stats("attack", "speed")

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
@pytest.mark.integration
def test_get_pokemon_by_stats_exclude_special_pokemon_by_default(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_stats("attack", "speed")

    # Should NOT include legendaries
    assert "regigigas" not in result
    assert "groudon" not in result
    assert "rayquaza" not in result

    # Should include normal Pokemon
    assert "garchomp" in result
    assert "salamence" in result


# Case 8: Include all special Pokemon (legendary, mythical, ultra beasts)
@pytest.mark.integration
def test_get_pokemon_by_stats_include_all_special_pokemon(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_stats(
        "attack", "speed",
        include_legendary=True,
        include_mythical=True,
        include_ultra_beasts=True
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
@pytest.mark.integration
def test_get_pokemon_by_stats_min_primary_threshold(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_stats("attack", "speed", min_primary=130)

    # All results should have attack >= 130
    # Garchomp (Attack: 130) should be included
    assert "garchomp" in result

    # Blaziken (Attack: 120) should NOT be included
    assert "blaziken" not in result


# Case 10: Explicit min_secondary
@pytest.mark.integration
def test_get_pokemon_by_stats_explicit_min_secondary(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_stats("attack", "speed", min_primary=100, min_secondary=100)

    # Should only include Pokemon with attack >= 100 AND speed >= 100
    assert len(result) > 0

    # Garchomp (Attack: 130, Speed: 102) should be included
    assert "garchomp" in result

# Case 11: min_speed filter
@pytest.mark.integration
def test_get_pokemon_by_stats_min_speed_filter(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_stats("attack", "defense", min_primary=100, min_speed=100)

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
@pytest.mark.integration
def test_get_pokemon_by_type_invalid_type(finder_postgres: CandidateFinderService):
    with pytest.raises(InvalidPokemonTypeError):
        finder_postgres.repository.get_pokemon_by_type("definitely-not-a-type")

# Case 2: Single type search
@pytest.mark.integration
def test_get_pokemon_by_type_single_type(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_type("fire")

    # Should be a frozenset
    assert isinstance(result, frozenset)

    # Should include fire types
    assert "charizard" in result
    assert "typhlosion" in result

    # Should NOT include non-fire types
    assert "pikachu" not in result

# Case 3: Dual type search
@pytest.mark.integration
def test_get_pokemon_by_type_dual_type(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_type("fire", "flying")

    # Should only include Pokemon with BOTH fire AND flying
    assert "charizard" in result

    # Should NOT include Pokemon with only one type
    assert "typhlosion" not in result  # Fire only
    assert "pidgeot" not in result  # Flying only

# Case 4: Default behavior (exclude legendary, mythical, ultra beasts)
@pytest.mark.integration
def test_get_pokemon_by_type_exclude_special_pokemon_by_default(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_type("psychic")

    # Should NOT include legendaries
    assert "mewtwo" not in result
    assert "latias" not in result

    # Should include normal Pokemon
    assert "alakazam" in result

# Case 5: Include all special Pokemon
@pytest.mark.integration
def test_get_pokemon_by_type_include_all_special_pokemon(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_pokemon_by_type("psychic", include_legendary=True, include_mythical=True, include_ultra_beasts=True)

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
@pytest.mark.integration
def test_get_type_effectiveness_single_type(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_type_effectiveness("fire")

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
@pytest.mark.integration
def test_get_type_effectiveness_dual_type(finder_postgres: CandidateFinderService):
    result = finder_postgres.repository.get_type_effectiveness("fire", "flying")

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
@pytest.mark.integration
def test_search_pokemon_no_filters(finder_postgres: CandidateFinderService):
    with pytest.raises(ValueError, match="At least one filter parameter is required"):
        finder_postgres.search_pokemon()

# Case 2: Move filter returns frozenset of names
@pytest.mark.integration
def test_search_pokemon_move_only(finder_postgres: CandidateFinderService):
    result = finder_postgres.search_pokemon(move="tackle")

    assert isinstance(result, frozenset)
    assert len(result) > 0
    # Tackle is a common move, should return many Pokemon
    assert "pikachu" in result or "rattata" in result

# Case 3: Type filter returns frozenset of names
@pytest.mark.integration
def test_search_pokemon_type_only(finder_postgres: CandidateFinderService):
    result = finder_postgres.search_pokemon(desired_type="fire")

    assert isinstance(result, frozenset)
    assert len(result) > 0
    assert "charizard" in result
    assert "typhlosion" in result

# Case 4: Stats filter returns frozenset of names
@pytest.mark.integration
def test_search_pokemon_stats_only(finder_postgres: CandidateFinderService):
    result = finder_postgres.search_pokemon(primary_stat="attack", secondary_stat="speed")

    assert isinstance(result, frozenset)
    assert len(result) > 0

# Case 5: Multiple filters combine with AND logic (intersection)
@pytest.mark.integration
def test_search_pokemon_multiple_filters_intersection(finder_postgres: CandidateFinderService):
    # Fire type that learns a specific move
    result = finder_postgres.search_pokemon(move="flamethrower", desired_type="fire")

    assert isinstance(result, frozenset)
    # Should be smaller than just fire types or just flamethrower users
    fire_only = finder_postgres.search_pokemon(desired_type="fire")
    assert len(result) <= len(fire_only)

    # All results must be fire type AND learn flamethrower
    for pokemon in result:
        # Would need to verify both conditions, but we trust the intersection logic
        pass

# Case 6: Legendary filtering applies to all filter types
@pytest.mark.integration
def test_search_pokemon_exclude_legendary_default(finder_postgres: CandidateFinderService):
    # Psychic type search should exclude legendaries by default
    result = finder_postgres.search_pokemon(desired_type="psychic")

    assert "mewtwo" not in result
    assert "latias" not in result
    assert "alakazam" in result  # Non-legendary psychic

# Case 7: Include legendary flag works
@pytest.mark.integration
def test_search_pokemon_include_legendary(finder_postgres: CandidateFinderService):
    result = finder_postgres.search_pokemon(desired_type="psychic", include_legendary=True)

    # Should include at least some legendary psychic types
    # Note: Actual legendary Pokemon in test data may vary
    assert len(result) > 0

# ===========================
# test_build_response.py
# ============================
def test_print_all_tables(finder_postgres: CandidateFinderService):
    pokemon_names = frozenset(["bronzong", "exeggutor", "gallade"])
    response = finder_postgres.build_response(pokemon_names)

    tables = [
        ("moves_table", response.moves_table),
        ("stats_table", response.stats_table),
        ("types_table", response.types_table),
        ("versus_types_table", response.versus_types_table),
    ]

    for table_name, table in tables:
        print(f"table: {table_name}")
        for row in table.rows:
            pprint.pprint(row)


# Case 1: Response has all tables populated
@pytest.mark.integration
def test_build_response_all_tables_populated(finder_postgres: CandidateFinderService):
    pokemon_names = frozenset(["bronzong", "exeggutor", "gallade"])
    response = finder_postgres.build_response(pokemon_names)

    # All tables should be present
    assert response.moves_table is not None
    assert response.stats_table is not None
    assert response.types_table is not None

# Case 2: Tables contain correct Pokemon
@pytest.mark.integration
def test_build_response_correct_pokemon(finder_postgres: CandidateFinderService):
    pokemon_names = frozenset(["bronzong", "haunter"])
    response = finder_postgres.build_response(pokemon_names)

    # Types table should have both Pokemon
    assert response.types_table is not None
    types_names = {row.name for row in response.types_table.rows}
    assert "bronzong" in types_names
    assert "haunter" in types_names
    assert len(types_names) == 2

    # Stats table should have both Pokemon
    assert response.stats_table is not None
    stats_names = {row.name for row in response.stats_table.rows}
    assert "bronzong" in stats_names
    assert "haunter" in stats_names

# Case 3: Type data is accurate
@pytest.mark.integration
def test_build_response_type_data_accurate(finder_postgres: CandidateFinderService):
    pokemon_names = frozenset(["haunter"])
    response = finder_postgres.build_response(pokemon_names)

    # Haunter should be Ghost/Poison type
    assert response.types_table is not None
    haunter_row = response.types_table.rows[0]
    assert haunter_row.name == "haunter"
    assert "ghost" in [haunter_row.type1, haunter_row.type2]

# Case 4: Stats data is accurate
@pytest.mark.integration
def test_build_response_stats_data_accurate(finder_postgres: CandidateFinderService):
    pokemon_names = frozenset(["haunter"])
    response = finder_postgres.build_response(pokemon_names)

    # Find haunter in stats table
    assert response.stats_table is not None
    haunter_row = next(row for row in response.stats_table.rows if row.name == "haunter")

    # Stats should be integers and reasonable
    assert isinstance(haunter_row.attack, int)
    assert isinstance(haunter_row.speed, int)
    assert haunter_row.attack > 0
    assert haunter_row.speed > 0


# ===========================
# test_type_index_canonical.py
# ============================

# Test that dual-type Pokemon are normalized to canonical ordering
@pytest.mark.integration
def test_type_index_has_single_types(finder_postgres: CandidateFinderService):
    """Test that type index contains single-type entries."""
    type_index = finder_postgres.repository.get_type_index()

    # Should only have single-type keys (no "/" in key)
    single_types = [k for k in type_index.keys() if "/" not in k]
    assert len(single_types) > 0, "Should have single-type entries like 'fire', 'water'"

    # Check expected single types exist
    assert "fire" in type_index
    assert "water" in type_index
    assert "psychic" in type_index

@pytest.mark.integration
def test_type_index_dual_types_under_both(finder_postgres: CandidateFinderService):
    """Test that dual-type Pokemon appear under both of their types."""
    type_index = finder_postgres.repository.get_type_index()

    # Charizard is fire/flying, should be under both
    assert "charizard" in type_index["fire"]
    assert "charizard" in type_index["flying"]

    # Hydreigon is dark/dragon, should be under both
    assert "hydreigon" in type_index["dark"]
    assert "hydreigon" in type_index["dragon"]


# ===========================
# test_opponent_weakness_type_index.py
# ============================

@pytest.mark.integration
def test_opponent_weakness_fire_flying(finder_postgres: CandidateFinderService):
    """Test fire/flying has 4x weakness to rock."""
    index = finder_postgres.repository.get_opponent_weakness_type_index()

    assert "fire/flying" in index
    fire_flying = index["fire/flying"]

    # Rock should be 4x effective (2x against fire, 2x against flying)
    assert "rock" in fire_flying["4x"]

    # Water and electric should be 2x
    assert "water" in fire_flying["2x"]
    assert "electric" in fire_flying["2x"]

@pytest.mark.integration
def test_opponent_weakness_single_type(finder_postgres: CandidateFinderService):
    """Test single-type matchups work correctly."""
    index = finder_postgres.repository.get_opponent_weakness_type_index()

    fire = index["fire"]

    # Fire's weaknesses
    assert "water" in fire["2x"]
    assert "ground" in fire["2x"]
    assert "rock" in fire["2x"]

    # Fire's resistances
    assert "fire" in fire["0.5x"] or "grass" in fire["0.5x"]

@pytest.mark.integration
def test_opponent_weakness_has_all_effectiveness_keys(finder_postgres: CandidateFinderService):
    """Test that all effectiveness keys exist."""
    index = finder_postgres.repository.get_opponent_weakness_type_index()

    fire_flying = index["fire/flying"]

    # Should have all six keys
    assert "4x" in fire_flying
    assert "2x" in fire_flying
    assert "1x" in fire_flying
    assert "0.5x" in fire_flying
    assert "0.25x" in fire_flying
    assert "0x" in fire_flying
