"""Unit tests for JSONRepository.

Split into two sections:
  1. Loader tests  — each _load_* method tested in isolation with mocked JSON data.
  2. Public method tests — get_* methods tested with pre-injected fake indexes.
"""

from unittest.mock import mock_open, patch

import pytest

from backend.src.lib.exceptions import (
    InvalidPokemonMoveError,
    InvalidPokemonStatError,
    InvalidPokemonTypeError,
    NoPokemonFoundError,
    TooManyTypesError,
)
from backend.src.lib.repository import JSONRepository

# ---------------------------------------------------------------------------
# Minimal JSON fixture payloads for loader tests
# ---------------------------------------------------------------------------

_POKEMON_FIXTURE = [
    {
        "name": "bulbasaur",
        "display_name": "Bulbasaur",
        "number": 1,
        "height": 7.0,
        "weight": 69.0,
        "sprite_url": "https://example.com/1.png",
        "description": "A strange seed.",
        "genus": "Seed Pokemon",
        "type_display": "grass/poison",
        "is_legendary": False,
        "is_mythical": False,
        "is_ultra_beast": False,
    },
    {
        "name": "mewtwo",
        "display_name": "Mewtwo",
        "number": 150,
        "height": 20.0,
        "weight": 1220.0,
        "sprite_url": "https://example.com/150.png",
        "description": "Created by science.",
        "genus": "Genetic Pokemon",
        "type_display": "psychic",
        "is_legendary": True,
        "is_mythical": False,
        "is_ultra_beast": False,
    },
]

_MOVE_FIXTURE = [
    {"pokemon_name": "bulbasaur", "move_name": "tackle", "learn_method": "level-up", "level": 1},
    {"pokemon_name": "bulbasaur", "move_name": "cut", "learn_method": "machine", "level": 0},
    {"pokemon_name": "mewtwo", "move_name": "tackle", "learn_method": "level-up", "level": 1},
]

_STATS_FIXTURE = [
    {
        "pokemon_name": "bulbasaur",
        "hp": 45,
        "attack": 49,
        "defense": 49,
        "special_attack": 65,
        "special_defense": 65,
        "speed": 45,
    },
    {
        "pokemon_name": "mewtwo",
        "hp": 106,
        "attack": 110,
        "defense": 90,
        "special_attack": 154,
        "special_defense": 90,
        "speed": 130,
    },
]

_STAT_SPREAD_FIXTURE = [
    {
        "stat_name": "hp",
        "percentile_20": 45,
        "percentile_40": 60,
        "percentile_60": 80,
        "percentile_80": 100,
        "percentile_100": 255,
        "median": 70,
    },
    {
        "stat_name": "attack",
        "percentile_20": 50,
        "percentile_40": 70,
        "percentile_60": 90,
        "percentile_80": 110,
        "percentile_100": 181,
        "median": 80,
    },
]

_TYPE_FIXTURE = [
    {"pokemon_name": "bulbasaur", "type_name": "grass", "slot": 1},
    {"pokemon_name": "bulbasaur", "type_name": "poison", "slot": 2},
    {"pokemon_name": "charmander", "type_name": "fire", "slot": 1},
]

# Minimal 3-type chart (fire, water, grass) — non-1x entries only
_TYPE_MATCHUP_FIXTURE = [
    {"defender_type": "fire", "attacker_type": "fire", "multiplier": 0.5},
    {"defender_type": "fire", "attacker_type": "water", "multiplier": 2.0},
    {"defender_type": "fire", "attacker_type": "grass", "multiplier": 0.5},
    {"defender_type": "water", "attacker_type": "fire", "multiplier": 0.5},
    {"defender_type": "water", "attacker_type": "water", "multiplier": 0.5},
    {"defender_type": "water", "attacker_type": "grass", "multiplier": 2.0},
    {"defender_type": "grass", "attacker_type": "fire", "multiplier": 2.0},
    {"defender_type": "grass", "attacker_type": "water", "multiplier": 0.5},
    {"defender_type": "grass", "attacker_type": "grass", "multiplier": 0.5},
]

_MACHINE_MOVES_FIXTURE = [
    {"name": "flamethrower", "machine_id": "TM35"},
    {"name": "cut", "machine_id": "TM15"},
    {"name": "splash", "machine_id": None},
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_repo() -> JSONRepository:
    """Instantiate JSONRepository without running __init__."""
    return JSONRepository.__new__(JSONRepository)


# fake_repo fixture is defined in conftest.py and uses tests/unit/fixtures/fake_data.py


# ===========================================================================
# Loader Tests
# ===========================================================================


@pytest.mark.unit
class TestLoadPokemonIndex:
    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_returns_dict_keyed_by_name(self, _mock_file, mock_load):
        mock_load.return_value = _POKEMON_FIXTURE
        repo = _make_repo()
        index = repo._load_pokemon_index()
        assert "bulbasaur" in index
        assert "mewtwo" in index

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_values_are_dicts_with_correct_fields(self, _mock_file, mock_load):
        mock_load.return_value = _POKEMON_FIXTURE
        repo = _make_repo()
        index = repo._load_pokemon_index()
        assert isinstance(index["bulbasaur"], dict)
        assert index["bulbasaur"]["display_name"] == "Bulbasaur"

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_legendary_flag_preserved(self, _mock_file, mock_load):
        mock_load.return_value = _POKEMON_FIXTURE
        repo = _make_repo()
        index = repo._load_pokemon_index()
        assert index["bulbasaur"]["is_legendary"] is False
        assert index["mewtwo"]["is_legendary"] is True

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_count_matches_fixture(self, _mock_file, mock_load):
        mock_load.return_value = _POKEMON_FIXTURE
        repo = _make_repo()
        index = repo._load_pokemon_index()
        assert len(index) == len(_POKEMON_FIXTURE)


@pytest.mark.unit
class TestLoadMoveIndex:
    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_returns_nested_dict_keyed_by_move(self, _mock_file, mock_load):
        mock_load.return_value = _MOVE_FIXTURE
        repo = _make_repo()
        index = repo._load_move_index()
        assert "tackle" in index
        assert "cut" in index

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_level_up_stored_as_level_int(self, _mock_file, mock_load):
        mock_load.return_value = _MOVE_FIXTURE
        repo = _make_repo()
        index = repo._load_move_index()
        assert index["tackle"]["bulbasaur"]["level-up"] == 1

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_machine_stored_as_true(self, _mock_file, mock_load):
        mock_load.return_value = _MOVE_FIXTURE
        repo = _make_repo()
        index = repo._load_move_index()
        assert index["cut"]["bulbasaur"]["machine"] is True

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_multiple_pokemon_under_same_move(self, _mock_file, mock_load):
        mock_load.return_value = _MOVE_FIXTURE
        repo = _make_repo()
        index = repo._load_move_index()
        assert "bulbasaur" in index["tackle"]
        assert "mewtwo" in index["tackle"]


@pytest.mark.unit
class TestLoadStatIndex:
    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_returns_dict_keyed_by_pokemon(self, _mock_file, mock_load):
        mock_load.return_value = _STATS_FIXTURE
        repo = _make_repo()
        index = repo._load_stat_index()
        assert "bulbasaur" in index
        assert "mewtwo" in index

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_all_six_stats_present(self, _mock_file, mock_load):
        mock_load.return_value = _STATS_FIXTURE
        repo = _make_repo()
        index = repo._load_stat_index()
        assert set(index["bulbasaur"].keys()) == {
            "hp",
            "attack",
            "defense",
            "special_attack",
            "special_defense",
            "speed",
        }

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_stat_values_correct(self, _mock_file, mock_load):
        mock_load.return_value = _STATS_FIXTURE
        repo = _make_repo()
        index = repo._load_stat_index()
        assert index["bulbasaur"]["hp"] == 45
        assert index["mewtwo"]["special_attack"] == 154


@pytest.mark.unit
class TestLoadStatSpreadIndex:
    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_returns_stat_medians_and_quintiles(self, _mock_file, mock_load):
        mock_load.return_value = _STAT_SPREAD_FIXTURE
        repo = _make_repo()
        index = repo._load_stat_spread_index()
        assert "STAT_MEDIANS" in index
        assert "QUINTILES" in index

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_medians_correct(self, _mock_file, mock_load):
        mock_load.return_value = _STAT_SPREAD_FIXTURE
        repo = _make_repo()
        index = repo._load_stat_spread_index()
        assert index["STAT_MEDIANS"]["hp"] == 70
        assert index["STAT_MEDIANS"]["attack"] == 80

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_quintiles_have_all_percentiles(self, _mock_file, mock_load):
        mock_load.return_value = _STAT_SPREAD_FIXTURE
        repo = _make_repo()
        index = repo._load_stat_spread_index()
        assert set(index["QUINTILES"]["hp"].keys()) == {"20th", "40th", "60th", "80th", "100th"}


@pytest.mark.unit
class TestLoadTypeIndex:
    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_returns_dict_keyed_by_type(self, _mock_file, mock_load):
        mock_load.return_value = _TYPE_FIXTURE
        repo = _make_repo()
        index = repo._load_type_index()
        assert "grass" in index
        assert "poison" in index
        assert "fire" in index

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_values_are_frozensets(self, _mock_file, mock_load):
        mock_load.return_value = _TYPE_FIXTURE
        repo = _make_repo()
        index = repo._load_type_index()
        assert isinstance(index["grass"], frozenset)

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_dual_type_pokemon_appears_under_both_types(self, _mock_file, mock_load):
        mock_load.return_value = _TYPE_FIXTURE
        repo = _make_repo()
        index = repo._load_type_index()
        assert "bulbasaur" in index["grass"]
        assert "bulbasaur" in index["poison"]

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_single_type_pokemon_appears_under_one_type(self, _mock_file, mock_load):
        mock_load.return_value = _TYPE_FIXTURE
        repo = _make_repo()
        index = repo._load_type_index()
        assert "charmander" in index["fire"]
        assert "charmander" not in index.get("grass", frozenset())


@pytest.mark.unit
class TestLoadOpponentWeaknessTypeIndex:
    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_contains_single_type_keys(self, _mock_file, mock_load):
        mock_load.return_value = _TYPE_MATCHUP_FIXTURE
        repo = _make_repo()
        repo.type_pairs = frozenset()
        index = repo._load_opponent_weakness_type_index()
        assert "fire" in index
        assert "water" in index
        assert "grass" in index

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_contains_dual_type_keys(self, _mock_file, mock_load):
        mock_load.return_value = _TYPE_MATCHUP_FIXTURE
        repo = _make_repo()
        repo.type_pairs = frozenset(["fire/water"])
        index = repo._load_opponent_weakness_type_index()
        assert "fire/water" in index

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_fire_is_weak_to_water(self, _mock_file, mock_load):
        mock_load.return_value = _TYPE_MATCHUP_FIXTURE
        repo = _make_repo()
        repo.type_pairs = frozenset()
        index = repo._load_opponent_weakness_type_index()
        assert "water" in index["fire"]["2x"]

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_effectiveness_buckets_are_frozensets(self, _mock_file, mock_load):
        mock_load.return_value = _TYPE_MATCHUP_FIXTURE
        repo = _make_repo()
        repo.type_pairs = frozenset()
        index = repo._load_opponent_weakness_type_index()
        for bucket in index["fire"].values():
            assert isinstance(bucket, frozenset)


@pytest.mark.unit
class TestLoadMyTeamStrengthsTypeIndex:
    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_contains_single_type_keys(self, _mock_file, mock_load):
        mock_load.return_value = _TYPE_MATCHUP_FIXTURE
        repo = _make_repo()
        repo.type_pairs = frozenset()
        index = repo._load_my_team_strengths_type_index()
        assert "fire" in index
        assert "water" in index
        assert "grass" in index

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_contains_dual_type_keys(self, _mock_file, mock_load):
        mock_load.return_value = _TYPE_MATCHUP_FIXTURE
        repo = _make_repo()
        repo.type_pairs = frozenset(["fire/water"])
        index = repo._load_my_team_strengths_type_index()
        assert "fire/water" in index

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_fire_is_effective_against_grass(self, _mock_file, mock_load):
        mock_load.return_value = _TYPE_MATCHUP_FIXTURE
        repo = _make_repo()
        repo.type_pairs = frozenset()
        index = repo._load_my_team_strengths_type_index()
        assert "grass" in index["fire"]["2x"]

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_effectiveness_buckets_are_frozensets(self, _mock_file, mock_load):
        mock_load.return_value = _TYPE_MATCHUP_FIXTURE
        repo = _make_repo()
        repo.type_pairs = frozenset()
        index = repo._load_my_team_strengths_type_index()
        for bucket in index["fire"].values():
            assert isinstance(bucket, frozenset)


@pytest.mark.unit
class TestLoadMachineMoves:
    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_returns_dict_keyed_by_move_name(self, _mock_file, mock_load):
        mock_load.return_value = _MACHINE_MOVES_FIXTURE
        repo = _make_repo()
        index = repo._load_machine_moves_index()
        assert "flamethrower" in index
        assert "cut" in index

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_machine_id_correct(self, _mock_file, mock_load):
        mock_load.return_value = _MACHINE_MOVES_FIXTURE
        repo = _make_repo()
        index = repo._load_machine_moves_index()
        assert index["flamethrower"] == "TM35"
        assert index["cut"] == "TM15"

    @patch("backend.src.lib.repository.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_null_machine_id_excluded(self, _mock_file, mock_load):
        mock_load.return_value = _MACHINE_MOVES_FIXTURE
        repo = _make_repo()
        index = repo._load_machine_moves_index()
        assert "splash" not in index


# ===========================================================================
# Public Method Tests
# ===========================================================================


@pytest.mark.unit
class TestGetPokemonByName:
    def test_found_returns_data(self, fake_repo):
        result = fake_repo.get_pokemon_by_name("charizard")
        assert result is not None

    def test_found_correct_pokemon(self, fake_repo):
        result = fake_repo.get_pokemon_by_name("pikachu")
        assert result["display_name"] == "Pikachu"

    def test_empty_string_raises(self, fake_repo):
        with pytest.raises(ValueError):
            fake_repo.get_pokemon_by_name("")

    def test_invalid_name_raises(self, fake_repo):
        with pytest.raises(InvalidPokemonMoveError):
            fake_repo.get_pokemon_by_name("notapokemon")


@pytest.mark.unit
class TestGetPokemonByMove:
    def test_found_returns_dict(self, fake_repo):
        result = fake_repo.get_pokemon_by_move("tackle")
        assert isinstance(result, dict)

    def test_found_correct_pokemon(self, fake_repo):
        result = fake_repo.get_pokemon_by_move("tackle")
        assert "pikachu" in result
        assert "typhlosion" in result

    def test_invalid_move_raises(self, fake_repo):
        with pytest.raises(InvalidPokemonMoveError):
            fake_repo.get_pokemon_by_move("hyperspace-fury")

    def test_empty_move_raises(self, fake_repo):
        with pytest.raises(ValueError):
            fake_repo.get_pokemon_by_move("")

    def test_wrong_type_raises(self, fake_repo):
        with pytest.raises(TypeError):
            fake_repo.get_pokemon_by_move(123)  # type: ignore[arg-type]

    def test_excludes_legendary_by_default(self, fake_repo):
        result = fake_repo.get_pokemon_by_move("psychic")
        assert "mewtwo" not in result
        assert "alakazam" in result

    def test_includes_legendary_when_flagged(self, fake_repo):
        result = fake_repo.get_pokemon_by_move("psychic", include_legendary=True)
        assert "mewtwo" in result


@pytest.mark.unit
class TestGetPokemonByStats:
    def test_returns_dict(self, fake_repo):
        result = fake_repo.get_pokemon_by_stats("attack", "speed")
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_empty_primary_stat_raises(self, fake_repo):
        with pytest.raises(InvalidPokemonStatError):
            fake_repo.get_pokemon_by_stats("", "speed")

    def test_empty_secondary_stat_raises(self, fake_repo):
        with pytest.raises(InvalidPokemonStatError):
            fake_repo.get_pokemon_by_stats("attack", "")

    def test_invalid_primary_stat_raises(self, fake_repo):
        with pytest.raises(InvalidPokemonStatError):
            fake_repo.get_pokemon_by_stats("coolness", "speed")

    def test_invalid_secondary_stat_raises(self, fake_repo):
        with pytest.raises(InvalidPokemonStatError):
            fake_repo.get_pokemon_by_stats("attack", "badness")

    def test_no_results_raises(self, fake_repo):
        with pytest.raises(NoPokemonFoundError):
            fake_repo.get_pokemon_by_stats("attack", "speed", min_primary=999)

    def test_excludes_legendary_by_default(self, fake_repo):
        result = fake_repo.get_pokemon_by_stats("attack", "speed")
        assert "mewtwo" not in result

    def test_includes_legendary_when_flagged(self, fake_repo):
        result = fake_repo.get_pokemon_by_stats("attack", "speed", include_legendary=True)
        assert "mewtwo" in result

    def test_ranked_by_primary_stat(self, fake_repo):
        result = fake_repo.get_pokemon_by_stats("special_attack", "speed", include_legendary=True)
        names = list(result.keys())
        # mewtwo (sp_atk: 154, speed: 130) should rank above alakazam (sp_atk: 135, speed: 120)
        assert names.index("mewtwo") < names.index("alakazam")

    def test_min_primary_threshold_applied(self, fake_repo):
        result = fake_repo.get_pokemon_by_stats("attack", "speed", min_primary=80)
        assert "pikachu" not in result  # attack: 55, below threshold

    def test_min_speed_filter_applied(self, fake_repo):
        result = fake_repo.get_pokemon_by_stats("attack", "defense", min_primary=49, min_speed=90)
        assert "bronzong" not in result  # speed: 33, below threshold


@pytest.mark.unit
class TestGetPokemonByType:
    def test_single_type_returns_frozenset(self, fake_repo):
        result = fake_repo.get_pokemon_by_type("fire")
        assert isinstance(result, frozenset)

    def test_single_type_correct_pokemon(self, fake_repo):
        result = fake_repo.get_pokemon_by_type("fire")
        assert "charizard" in result
        assert "typhlosion" in result

    def test_dual_type_returns_intersection(self, fake_repo):
        result = fake_repo.get_pokemon_by_type("fire", "flying")
        assert "charizard" in result
        assert "typhlosion" not in result

    def test_invalid_type_raises(self, fake_repo):
        with pytest.raises(InvalidPokemonTypeError):
            fake_repo.get_pokemon_by_type("faketype")

    def test_too_many_types_raises(self, fake_repo):
        with pytest.raises(TooManyTypesError):
            fake_repo.get_pokemon_by_type("fire", "grass", "water")

    def test_no_types_raises(self, fake_repo):
        with pytest.raises(ValueError):
            fake_repo.get_pokemon_by_type()

    def test_excludes_legendary_by_default(self, fake_repo):
        result = fake_repo.get_pokemon_by_type("psychic")
        assert "mewtwo" not in result

    def test_excludes_mythical_by_default(self, fake_repo):
        result = fake_repo.get_pokemon_by_type("psychic")
        assert "celebi" not in result

    def test_includes_legendary_when_flagged(self, fake_repo):
        result = fake_repo.get_pokemon_by_type("psychic", include_legendary=True)
        assert "mewtwo" in result

    def test_includes_mythical_when_flagged(self, fake_repo):
        result = fake_repo.get_pokemon_by_type("psychic", include_mythical=True)
        assert "celebi" in result

    def test_includes_ultra_beast_when_flagged(self, fake_repo):
        result = fake_repo.get_pokemon_by_type("poison", include_ultra_beasts=True)
        assert "nihilego" in result


@pytest.mark.unit
class TestGetTypeEffectiveness:
    def test_single_type_returns_dict(self, fake_repo):
        result = fake_repo.get_type_effectiveness("fire")
        assert isinstance(result, dict)

    def test_single_type_correct_weaknesses(self, fake_repo):
        result = fake_repo.get_type_effectiveness("fire")
        assert "water" in result["2x"]

    def test_dual_type_returns_dict(self, fake_repo):
        result = fake_repo.get_type_effectiveness("fire", "flying")
        assert isinstance(result, dict)

    def test_dual_type_stacked_weakness(self, fake_repo):
        result = fake_repo.get_type_effectiveness("fire", "flying")
        assert "rock" in result["4x"]

    def test_dual_type_stacked_resistance(self, fake_repo):
        result = fake_repo.get_type_effectiveness("fire", "flying")
        assert "grass" in result["0.25x"]

    def test_dual_type_immunity(self, fake_repo):
        result = fake_repo.get_type_effectiveness("fire", "flying")
        assert "ground" in result["0x"]

    def test_no_types_raises(self, fake_repo):
        with pytest.raises(ValueError):
            fake_repo.get_type_effectiveness()

    def test_too_many_types_raises(self, fake_repo):
        with pytest.raises(TooManyTypesError):
            fake_repo.get_type_effectiveness("fire", "water", "grass")

    def test_invalid_type_raises(self, fake_repo):
        with pytest.raises(InvalidPokemonTypeError):
            fake_repo.get_type_effectiveness("faketype")

    def test_reversed_type_pair_also_works(self, fake_repo):
        result = fake_repo.get_type_effectiveness("flying", "fire")
        assert isinstance(result, dict)


@pytest.mark.unit
class TestValidatePokemonTypes:
    def test_valid_single_type_passes(self, fake_repo):
        fake_repo.validate_pokemon_types("fire")  # should not raise

    def test_valid_multiple_types_pass(self, fake_repo):
        fake_repo.validate_pokemon_types("fire", "grass")  # should not raise

    def test_invalid_type_raises(self, fake_repo):
        with pytest.raises(InvalidPokemonTypeError):
            fake_repo.validate_pokemon_types("faketype")

    def test_mixed_valid_and_invalid_raises(self, fake_repo):
        with pytest.raises(InvalidPokemonTypeError):
            fake_repo.validate_pokemon_types("fire", "faketype")
