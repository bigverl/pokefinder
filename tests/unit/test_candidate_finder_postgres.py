# PostgreSQL version of all candidate finder tests using function-scoped fixtures

import pytest
from backend.src.lib.exceptions import (
    NoPokemonFoundError,
    InvalidPokemonMoveError,
    InvalidPokemonTypeError
)

# ===========================
# test_get_pokemon_by_move.py
# ============================

# Case 1: Incorrect arg datatype (Programmer mistake)
@pytest.mark.unit_postgres
def test_get_pokemon_by_move_incorrect_argument_datatype_pg(finder_postgres):
    with pytest.raises(TypeError):
        finder_postgres.get_pokemon_by_move(123) # type: ignore

# Case 2: Move does not exist
@pytest.mark.unit_postgres
def test_get_pokemon_by_move_invalid_pokemon_types_pg(finder_postgres):
    with pytest.raises(InvalidPokemonMoveError):
        finder_postgres.get_pokemon_by_move("definitely not a move")

# Case 3: Found
@pytest.mark.unit_postgres
def test_get_pokemon_by_move_found_single_type_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_move("hypnosis")
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
@pytest.mark.unit_postgres
def test_get_pokemon_by_move_exclude_legendary_and_mythical_by_default_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_move("psychic")
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
@pytest.mark.unit_postgres
def test_get_pokemon_by_move_include_legendary_and_mythical_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_move("psychic", include_legendary=True, include_mythical=True)
    # Should include legendaries
    assert "latias" in result
    assert "cresselia" in result
    # Should include mythicals
    assert "celebi" in result
    assert "jirachi" in result
    # Should include normal Pokemon
    assert "alakazam" in result

# Case 6: Include all special Pokemon (legendary, mythical, ultra beasts)
@pytest.mark.unit_postgres
def test_get_pokemon_by_move_include_all_special_pokemon_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_move("psychic", include_legendary=True, include_mythical=True, include_ultra_beasts=True)
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

# Case 1: Incorrect argument datatype (Programmer mistake)
@pytest.mark.unit_postgres
def test_get_pokemon_by_stats_incorrect_stat_datatype_pg(finder_postgres):
    with pytest.raises(TypeError):
        finder_postgres.get_pokemon_by_stats(123, "speed")  # type: ignore


# Case 2: Empty stat names (Caller mistake)
@pytest.mark.unit_postgres
def test_get_pokemon_by_stats_empty_primary_stat_pg(finder_postgres):
    with pytest.raises(ValueError, match="primary_stat cannot be empty"):
        finder_postgres.get_pokemon_by_stats("", "speed")

@pytest.mark.unit_postgres
def test_get_pokemon_by_stats_empty_secondary_stat_pg(finder_postgres):
    with pytest.raises(ValueError, match="secondary_stat cannot be empty"):
        finder_postgres.get_pokemon_by_stats("attack", "")


# Case 3: Invalid stat names (Caller mistake)
@pytest.mark.unit_postgres
def test_get_pokemon_by_stats_invalid_primary_stat_pg(finder_postgres):
    with pytest.raises(ValueError, match="Invalid primary_stat"):
        finder_postgres.get_pokemon_by_stats("coolness", "speed")

@pytest.mark.unit_postgres
def test_get_pokemon_by_stats_invalid_secondary_stat_pg(finder_postgres):
    with pytest.raises(ValueError, match="Invalid secondary_stat"):
        finder_postgres.get_pokemon_by_stats("attack", "badness")


# Case 4: Valid search with default parameters
@pytest.mark.unit_postgres
def test_get_pokemon_by_stats_basic_attack_speed_search_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_stats("attack", "speed")

    # Should return a dict
    assert isinstance(result, dict)

    # Should have results
    assert len(result) > 0

    # Should have at least 5 results
    assert len(result) >= 5


# Case 5: No Pokemon found (threshold too high)
@pytest.mark.unit_postgres
def test_get_pokemon_by_stats_no_pokemon_found_high_threshold_pg(finder_postgres):
    with pytest.raises(NoPokemonFoundError):
        # No Pokemon has 200 attack and 200 speed
        finder_postgres.get_pokemon_by_stats("attack", "speed", min_primary=200, min_secondary=200)


# Case 6: Ranking order (weighted 70/30)
@pytest.mark.unit_postgres
def test_get_pokemon_by_stats_ranking_order_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_stats("attack", "speed")

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
@pytest.mark.unit_postgres
def test_get_pokemon_by_stats_exclude_special_pokemon_by_default_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_stats("attack", "speed")

    # Should NOT include legendaries
    assert "regigigas" not in result
    assert "groudon" not in result
    assert "rayquaza" not in result

    # Should include normal Pokemon
    assert "garchomp" in result
    assert "salamence" in result


# Case 8: Include all special Pokemon (legendary, mythical, ultra beasts)
@pytest.mark.unit_postgres
def test_get_pokemon_by_stats_include_all_special_pokemon_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_stats(
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
@pytest.mark.unit_postgres
def test_get_pokemon_by_stats_min_primary_threshold_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_stats("attack", "speed", min_primary=130)

    # All results should have attack >= 130
    # Garchomp (Attack: 130) should be included
    assert "garchomp" in result

    # Blaziken (Attack: 120) should NOT be included
    assert "blaziken" not in result


# Case 10: Explicit min_secondary
@pytest.mark.unit_postgres
def test_get_pokemon_by_stats_explicit_min_secondary_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_stats("attack", "speed", min_primary=100, min_secondary=100)

    # Should only include Pokemon with attack >= 100 AND speed >= 100
    assert len(result) > 0

    # Garchomp (Attack: 130, Speed: 102) should be included
    assert "garchomp" in result

# Case 11: min_speed filter
@pytest.mark.unit_postgres
def test_get_pokemon_by_stats_min_speed_filter_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_stats("attack", "defense", min_primary=100, min_speed=100)

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
@pytest.mark.unit_postgres
def test_get_pokemon_by_type_invalid_type_pg(finder_postgres):
    with pytest.raises(InvalidPokemonTypeError):
        finder_postgres.get_pokemon_by_type("definitely-not-a-type")

# Case 2: Single type search
@pytest.mark.unit_postgres
def test_get_pokemon_by_type_single_type_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_type("fire")

    # Should be a frozenset
    assert isinstance(result, frozenset)

    # Should include fire types
    assert "charizard" in result
    assert "typhlosion" in result

    # Should NOT include non-fire types
    assert "pikachu" not in result

# Case 3: Dual type search
@pytest.mark.unit_postgres
def test_get_pokemon_by_type_dual_type_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_type("fire", "flying")

    # Should only include Pokemon with BOTH fire AND flying
    assert "charizard" in result

    # Should NOT include Pokemon with only one type
    assert "typhlosion" not in result  # Fire only
    assert "pidgeot" not in result  # Flying only

# Case 4: Default behavior (exclude legendary, mythical, ultra beasts)
@pytest.mark.unit_postgres
def test_get_pokemon_by_type_exclude_special_pokemon_by_default_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_type("psychic")

    # Should NOT include legendaries
    assert "mewtwo" not in result
    assert "latias" not in result

    # Should include normal Pokemon
    assert "alakazam" in result

# Case 5: Include all special Pokemon
@pytest.mark.unit_postgres
def test_get_pokemon_by_type_include_all_special_pokemon_pg(finder_postgres):
    result = finder_postgres.get_pokemon_by_type("psychic", include_legendary=True, include_mythical=True, include_ultra_beasts=True)

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
@pytest.mark.unit_postgres
def test_get_type_effectiveness_single_type_pg(finder_postgres):
    result = finder_postgres.get_type_effectiveness("fire")

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
@pytest.mark.unit_postgres
def test_get_type_effectiveness_dual_type_pg(finder_postgres):
    result = finder_postgres.get_type_effectiveness("fire", "flying")

    # Fire/Flying is 4x weak to rock (2x from fire * 2x from flying = 4x)
    assert "rock" in result["4x"]

    # Water is 2x effective (fire weakness, flying neutral)
    assert "water" in result["2x"]

    # Grass is 0.25x effective (fire resists, flying resists)
    assert "grass" in result["0.25x"]
