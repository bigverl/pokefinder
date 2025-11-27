
import pytest
from backend.candidate_finder.exceptions import (
    NoPokemonFoundError,
    InvalidPokemonMoveError
)

# ===========================
# test_get_pokemon_by_move.py
# ============================

# Case 1: Incorrect arg datatype (Programmer mistake)
def test_get_pokemon_by_move_incorrect_argument_datatype(finder):
    with pytest.raises(TypeError):
        finder.get_pokemon_by_move(123) # type: ignore

# Case 2: Move does not exist
def test_get_pokemon_by_move_invalid_pokemon_types(finder):
    with pytest.raises(InvalidPokemonMoveError):
        finder.get_pokemon_by_move("definitely not a move")

# Case 3: Found
def test_get_pokemon_by_move_found_single_type(finder):
    result = finder.get_pokemon_by_move("hypnosis")
    # Ultra Beasts (xurkitree, blacephalon) are excluded by default
    assert result == {
        'vulpix': {'egg': True}, 'zubat': {'egg': True},
        'meowth': {'egg': True}, 'psyduck': {'egg': True},
        'poliwag': {'level-up': 1}, 'poliwhirl': {'level-up': 1},
        'poliwrath': {'level-up': 1}, 'ponyta': {'egg': True},
        'gastly': {'level-up': 4}, 'haunter': {'level-up': 1},
        'gengar': {'level-up': 1}, 'exeggcute': {'level-up': 1},
        'exeggutor': {'level-up': 1}, 'mr-mime': {'egg': True},
        'hoothoot': {'level-up': 36}, 'noctowl': {'level-up': 48},
        'politoed': {'level-up': 1}, 'ralts': {'level-up': 9},
        'kirlia': {'level-up': 9}, 'gardevoir': {'level-up': 9},
        'lunatone': {'level-up': 5}, 'solrock': {'level-up': 5},
        'feebas': {'egg': True}, 'drifloon': {'egg': True},
        'bronzor': {'level-up': 20}, 'bronzong': {'level-up': 20},
        'mime-jr': {'egg': True}, 'spiritomb': {'level-up': 55},
        'gallade': {'level-up': 1}, 'munna': {'level-up': 4},
        'musharna': {'level-up': 1}, 'pidove': {'egg': True},
        'sigilyph': {'level-up': 10}, 'gothita': {'level-up': 24},
        'gothorita': {'level-up': 24}, 'gothitelle': {'level-up': 24},
        'inkay': {'level-up': 3}, 'malamar': {'level-up': 1},
        'sandygast': {'level-up': 30}, 'palossand': {'level-up': 30}
    }

# Case 4: Legendary/Mythical filtering - Default (exclude both)
def test_get_pokemon_by_move_exclude_legendary_and_mythical_by_default(finder):
    result = finder.get_pokemon_by_move("psychic")
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
def test_get_pokemon_by_move_include_legendary_and_mythical(finder):
    result = finder.get_pokemon_by_move("psychic", include_legendary=True, include_mythical=True)
    # Should include legendaries
    assert "latias" in result
    assert "cresselia" in result
    # Should include mythicals
    assert "celebi" in result
    assert "jirachi" in result
    # Should include normal Pokemon
    assert "alakazam" in result

# Case 6: Include all special Pokemon (legendary, mythical, ultra beasts)
def test_get_pokemon_by_move_include_all_special_pokemon(finder):
    result = finder.get_pokemon_by_move("psychic", include_legendary=True, include_mythical=True, include_ultra_beasts=True)
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
def test_get_pokemon_by_stats_incorrect_stat_datatype(finder):
    with pytest.raises(TypeError):
        finder.get_pokemon_by_stats(123, "speed")  # type: ignore


# Case 2: Empty stat names (Caller mistake)
def test_get_pokemon_by_stats_empty_primary_stat(finder):
    with pytest.raises(ValueError, match="primary_stat cannot be empty"):
        finder.get_pokemon_by_stats("", "speed")


def test_get_pokemon_by_stats_empty_secondary_stat(finder):
    with pytest.raises(ValueError, match="secondary_stat cannot be empty"):
        finder.get_pokemon_by_stats("attack", "")


# Case 3: Invalid stat names (Caller mistake)
def test_get_pokemon_by_stats_invalid_primary_stat(finder):
    with pytest.raises(ValueError, match="Invalid primary_stat"):
        finder.get_pokemon_by_stats("coolness", "speed")


def test_get_pokemon_by_stats_invalid_secondary_stat(finder):
    with pytest.raises(ValueError, match="Invalid secondary_stat"):
        finder.get_pokemon_by_stats("attack", "badness")


# Case 4: Valid search with default parameters
def test_get_pokemon_by_stats_basic_attack_speed_search(finder):
    result = finder.get_pokemon_by_stats("attack", "speed")

    # Should return a list
    assert isinstance(result, list)

    # Should have results
    assert len(result) > 0

    # Should be ordered (best first)
    assert len(result) >= 5  # Should have at least 5 results


# Case 5: No Pokemon found (threshold too high)
def test_get_pokemon_by_stats_no_pokemon_found_high_threshold(finder):
    with pytest.raises(NoPokemonFoundError):
        # No Pokemon has 200 attack and 200 speed
        finder.get_pokemon_by_stats("attack", "speed", min_primary=200, min_secondary=200)


# Case 6: Ranking order (weighted 70/30)
def test_get_pokemon_by_stats_ranking_order(finder):
    result = finder.get_pokemon_by_stats("attack", "speed")

    # Slaking (Attack: 160, Speed: 100) should rank very high
    # Garchomp (Attack: 130, Speed: 102) should also be in top results
    assert "slaking" in result[:10]
    assert "garchomp" in result[:20]


# Case 7: Default behavior (exclude legendary, mythical, ultra beasts)
def test_get_pokemon_by_stats_exclude_special_pokemon_by_default(finder):
    result = finder.get_pokemon_by_stats("attack", "speed")

    # Should NOT include legendaries
    assert "regigigas" not in result
    assert "groudon" not in result
    assert "rayquaza" not in result

    # Should include normal Pokemon
    assert "garchomp" in result
    assert "salamence" in result


# Case 8: Include all special Pokemon (legendary, mythical, ultra beasts)
def test_get_pokemon_by_stats_include_all_special_pokemon(finder):
    result = finder.get_pokemon_by_stats(
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
def test_get_pokemon_by_stats_min_primary_threshold(finder):
    result = finder.get_pokemon_by_stats("attack", "speed", min_primary=130)

    # All results should have attack >= 130
    # Garchomp (Attack: 130) should be included
    assert "garchomp" in result

    # Blaziken (Attack: 120) should NOT be included
    assert "blaziken" not in result


# Case 10: Explicit min_secondary
def test_get_pokemon_by_stats_explicit_min_secondary(finder):
    result = finder.get_pokemon_by_stats("attack", "speed", min_primary=100, min_secondary=100)

    # Should only include Pokemon with attack >= 100 AND speed >= 100
    assert len(result) > 0

    # Garchomp (Attack: 130, Speed: 102) should be included
    assert "garchomp" in result

# Case 11: min_speed filter
def test_get_pokemon_by_stats_min_speed_filter(finder):
    result = finder.get_pokemon_by_stats("attack", "defense", min_primary=100, min_speed=100)

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
def test_get_pokemon_by_type_invalid_type(finder):
    from backend.candidate_finder.exceptions import InvalidPokemonTypeError
    with pytest.raises(InvalidPokemonTypeError):
        finder.get_pokemon_by_type("definitely-not-a-type")

# Case 2: Single type search
def test_get_pokemon_by_type_single_type(finder):
    result = finder.get_pokemon_by_type("fire")

    # Should be a frozenset
    assert isinstance(result, frozenset)

    # Should include fire types
    assert "charizard" in result
    assert "typhlosion" in result

    # Should NOT include non-fire types
    assert "pikachu" not in result

# Case 3: Dual type search
def test_get_pokemon_by_type_dual_type(finder):
    result = finder.get_pokemon_by_type("fire", "flying")

    # Should only include Pokemon with BOTH fire AND flying
    assert "charizard" in result

    # Should NOT include Pokemon with only one type
    assert "typhlosion" not in result  # Fire only
    assert "pidgeot" not in result  # Flying only

# Case 4: Default behavior (exclude legendary, mythical, ultra beasts)
def test_get_pokemon_by_type_exclude_special_pokemon_by_default(finder):
    result = finder.get_pokemon_by_type("psychic")

    # Should NOT include legendaries
    assert "mewtwo" not in result
    assert "latias" not in result

    # Should include normal Pokemon
    assert "alakazam" in result

# Case 5: Include all special Pokemon
def test_get_pokemon_by_type_include_all_special_pokemon(finder):
    result = finder.get_pokemon_by_type("psychic", include_legendary=True, include_mythical=True, include_ultra_beasts=True)

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
def test_get_type_effectiveness_single_type(finder):
    result = finder.get_type_effectiveness("fire")

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
def test_get_type_effectiveness_dual_type(finder):
    result = finder.get_type_effectiveness("fire", "flying")

    # Fire/Flying is 4x weak to rock (2x from fire * 2x from flying = 4x)
    assert "rock" in result["4x"]

    # Water is 2x effective (fire weakness, flying neutral)
    assert "water" in result["2x"]

    # Grass is 0.25x effective (fire resists, flying resists)
    assert "grass" in result["0.25x"]
