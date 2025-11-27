
import pytest

def test_json_repository_get_move_index(json_repo):
    move_index = json_repo.get_move_index()

    # Verify structure exists and is not empty
    assert isinstance(move_index, dict)
    assert len(move_index) > 0

    # Check known moves exist
    assert "swords_dance" in move_index

    # Verify move data structure: {move_name: {pokemon_name: {method: value}}}
    swords_dance = move_index["swords_dance"]
    assert isinstance(swords_dance, dict)
    assert "bulbasaur" in swords_dance

    # Verify Pokemon entry structure
    bulbasaur_entry = swords_dance["bulbasaur"]
    assert isinstance(bulbasaur_entry, dict)
    assert "machine" in bulbasaur_entry or "level-up" in bulbasaur_entry

def test_json_repository_get_species_index(json_repo):
    species_index = json_repo.get_species_index()

    # Verify structure exists and is not empty
    assert isinstance(species_index, dict)
    assert len(species_index) > 0

    # Check known Pokemon exist
    assert "bulbasaur" in species_index
    assert "charizard" in species_index
    assert "mewtwo" in species_index

    # Verify species data structure: only has legendary/mythical/ultra_beast flags
    bulbasaur = species_index["bulbasaur"]
    assert isinstance(bulbasaur, dict)
    assert "is_legendary" in bulbasaur
    assert "is_mythical" in bulbasaur
    assert "is_ultra_beast" in bulbasaur
    assert bulbasaur["is_legendary"] == False

def test_json_repository_get_stat_index(json_repo):
    stat_index = json_repo.get_stat_index()

    # Verify structure exists and is not empty
    assert isinstance(stat_index, dict)
    assert len(stat_index) > 0

    # Check known Pokemon exist
    assert "pikachu" in stat_index
    assert "charizard" in stat_index

    # Verify stat data structure with normalized names (special_attack not special-attack)
    pikachu_stats = stat_index["pikachu"]
    assert isinstance(pikachu_stats, dict)
    assert "hp" in pikachu_stats
    assert "attack" in pikachu_stats
    assert "defense" in pikachu_stats
    assert "special_attack" in pikachu_stats
    assert "special_defense" in pikachu_stats
    assert "speed" in pikachu_stats

    # Verify stats are integers
    assert isinstance(pikachu_stats["hp"], int)
    assert pikachu_stats["speed"] > 0

def test_json_repository_get_stat_spread_index(json_repo):
    stat_spread_index = json_repo.get_stat_spread_index()

    # Verify structure exists
    assert isinstance(stat_spread_index, dict)

    # Check for required top-level keys
    assert "STAT_MEDIANS" in stat_spread_index
    assert "QUINTILES" in stat_spread_index

    # Verify STAT_MEDIANS structure
    medians = stat_spread_index["STAT_MEDIANS"]
    assert isinstance(medians, dict)
    assert "hp" in medians
    assert "attack" in medians
    assert "defense" in medians
    assert "special_attack" in medians
    assert "special_defense" in medians
    assert isinstance(medians["hp"], int)

    # Verify QUINTILES structure: {stat: {percentile: value}}
    quintiles = stat_spread_index["QUINTILES"]
    assert isinstance(quintiles, dict)
    assert "hp" in quintiles
    assert "attack" in quintiles
    assert "special_attack" in quintiles

    # Verify percentile structure
    hp_quintiles = quintiles["hp"]
    assert isinstance(hp_quintiles, dict)
    assert "20th" in hp_quintiles
    assert "40th" in hp_quintiles
    assert "60th" in hp_quintiles
    assert "80th" in hp_quintiles
    assert "100th" in hp_quintiles
    assert isinstance(hp_quintiles["20th"], int)

def test_json_repository_get_type_index(json_repo):
    type_index = json_repo.get_type_index()

    # Verify structure exists and is not empty
    assert isinstance(type_index, dict)
    assert len(type_index) > 0

    # Check known types exist
    assert "fire" in type_index
    assert "water" in type_index
    assert "electric" in type_index
    assert "grass" in type_index

    # Verify type data contains frozensets (not lists)
    fire_pokemon = type_index["fire"]
    assert isinstance(fire_pokemon, frozenset)
    assert "charizard" in fire_pokemon
    assert "charmander" in fire_pokemon

def test_json_repository_get_type_matchup_index(json_repo):
    type_matchup_index = json_repo.get_type_matchup_index()

    # Verify structure exists and is not empty
    assert isinstance(type_matchup_index, dict)
    assert len(type_matchup_index) > 0

    # Check known types exist
    assert "fire" in type_matchup_index
    assert "water" in type_matchup_index

    # Verify matchup structure uses damage field names (not 2x/0.5x)
    fire_matchup = type_matchup_index["fire"]
    assert isinstance(fire_matchup, dict)
    assert "double_damage_from" in fire_matchup
    assert "half_damage_from" in fire_matchup
    assert "no_damage_from" in fire_matchup

    # Verify matchup values are frozensets (not lists)
    assert isinstance(fire_matchup["double_damage_from"], frozenset)
    assert isinstance(fire_matchup["half_damage_from"], frozenset)

    # Verify known type effectiveness
    assert "water" in fire_matchup["double_damage_from"]  # Fire takes double damage from water
    assert "grass" in fire_matchup["half_damage_from"]  # Fire takes half damage from grass

def test_json_repository_get_machine_moves_index(json_repo):
    machine_moves_index = json_repo.get_machine_moves_index()

    # Verify structure exists and is not empty
    assert isinstance(machine_moves_index, dict)
    assert len(machine_moves_index) > 0

    # Verify structure: {move_name: tm_id}
    assert "mega_kick" in machine_moves_index
    assert machine_moves_index["mega_kick"] == "tm01"

    # Verify all values are TM/HM/TR identifiers
    for move_name, machine_id in machine_moves_index.items():
        assert isinstance(move_name, str)
        assert isinstance(machine_id, str)
        assert machine_id.startswith("tm") or machine_id.startswith("hm") or machine_id.startswith("tr")