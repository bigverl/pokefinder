"""Mock repository for unit testing - provides minimal test data for fast tests."""

from typing import Any
from backend.candidate_finder.repository import PokemonRepository


class MockPokemonRepository(PokemonRepository):
    """Test double with minimal, predictable data for unit testing."""

    def __init__(self):
        super().__init__()

    def get_type_index(self) -> dict[str, frozenset[str]]:
        """Returns minimal type index for testing."""
        return {
            "fire": frozenset({
                "charizard", "arcanine", "moltres", "entei", "ho-oh",
                "victini", "volcanion", "fletchinder", "talonflame", "typhlosion"
            }),
            "flying": frozenset({
                "charizard", "moltres", "ho-oh", "fletchinder",
                "talonflame", "celesteela"
            }),
            "ghost": frozenset({
                'phantump', 'golurk', 'shuppet', 'sandygast',
                'trevenant', 'golett', 'froslass', 'honedge', 'haunter', 'misdreavus',
                'cofagrigus', 'dhelmise', 'gastly', 'sableye', 'mismagius', 'litwick',
                'chandelure', 'shedinja', 'lampent', 'palossand', 'banette',
                'doublade', 'yamask', 'rotom', 'spiritomb', 'decidueye', 'gengar',
                'duskull', 'drifblim', 'dusclops', 'drifloon', 'dusknoir',
                'jellicent'
            }),
            "steel": frozenset({
                "steelix", "metagross", "kartana", "celesteela",
                "registeel", "magearna"
            }),
            "water": frozenset({
                "blastoise", "gyarados"
            }),
            "normal": frozenset({
                "slaking", "snorlax"
            }),
            "ice": frozenset({
                "glaceon", "avalugg"
            }),
            "psychic": frozenset({
                "mewtwo", "latias", "celebi", "alakazam"
            }),
        }

    def get_species_index(self) -> dict[str, dict[str, bool]]:
        """Returns species flags for test Pokemon."""
        return {
            # Fire Pokemon
            "charizard": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "arcanine": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "moltres": {"is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "entei": {"is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "ho-oh": {"is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "victini": {"is_legendary": False, "is_mythical": True, "is_ultra_beast": False},
            "volcanion": {"is_legendary": False, "is_mythical": True, "is_ultra_beast": False},
            "fletchinder": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "talonflame": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "typhlosion": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},

            # Steel Pokemon
            "steelix": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "metagross": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "kartana": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": True},
            "celesteela": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": True},
            "registeel": {"is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "magearna": {"is_legendary": False, "is_mythical": True, "is_ultra_beast": False},

            # Ghost Pokemon (all non-special for simplicity)
            'phantump': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'golurk': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'shuppet': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'sandygast': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'trevenant': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'golett': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'froslass': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'honedge': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'haunter': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'misdreavus': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'cofagrigus': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'dhelmise': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'gastly': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'sableye': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'mismagius': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'litwick': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'chandelure': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'shedinja': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'lampent': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'palossand': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'banette': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'doublade': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'yamask': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'rotom': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'spiritomb': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'decidueye': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'gengar': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'duskull': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'drifblim': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'dusclops': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'drifloon': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'dusknoir': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'jellicent': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},

            # Move test Pokemon
            "alakazam": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "latias": {"is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "latios": {"is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "cresselia": {"is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "celebi": {"is_legendary": False, "is_mythical": True, "is_ultra_beast": False},
            "jirachi": {"is_legendary": False, "is_mythical": True, "is_ultra_beast": False},
            "nihilego": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": True},
            "blacephalon": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": True},

            # Hypnosis move learners
            'vulpix': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'zubat': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'meowth': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'psyduck': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'poliwag': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'poliwhirl': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'poliwrath': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'ponyta': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'exeggcute': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'exeggutor': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'mr-mime': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'hoothoot': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'noctowl': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'politoed': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'ralts': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'kirlia': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'gardevoir': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'lunatone': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'solrock': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'feebas': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'bronzor': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'bronzong': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'mime-jr': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'gallade': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'munna': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'musharna': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'pidove': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'sigilyph': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'gothita': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'gothorita': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'gothitelle': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'inkay': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            'malamar': {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},

            # Stats test Pokemon
            "garchomp": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "salamence": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "slaking": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "blaziken": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "regigigas": {"is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "groudon": {"is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "rayquaza": {"is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
            "pheromosa": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": True},
            "aggron": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "rhyperior": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "dragonite": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},

            # Other
            "blastoise": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "gyarados": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "snorlax": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "glaceon": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "avalugg": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            "mewtwo": {"is_legendary": True, "is_mythical": False, "is_ultra_beast": False},
        }

    def get_move_index(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Returns minimal move index for testing."""
        return {
            "hypnosis": {
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
            },
            "psychic": {
                "alakazam": {'machine': True},
                "latias": {'machine': True},
                "latios": {'machine': True},
                "cresselia": {'machine': True},
                "celebi": {'machine': True},
                "jirachi": {'machine': True},
                "nihilego": {'machine': True},
                "blacephalon": {'machine': True},
            }
        }

    def get_stat_index(self) -> dict[str, dict[str, int]]:
        """Returns base stats for test Pokemon."""
        return {
            "garchomp": {"hp": 108, "attack": 130, "defense": 95, "special_attack": 80, "special_defense": 85, "speed": 102},
            "salamence": {"hp": 95, "attack": 135, "defense": 80, "special_attack": 110, "special_defense": 80, "speed": 100},
            "slaking": {"hp": 150, "attack": 160, "defense": 100, "special_attack": 95, "special_defense": 65, "speed": 100},
            "blaziken": {"hp": 80, "attack": 120, "defense": 70, "special_attack": 110, "special_defense": 70, "speed": 80},
            "regigigas": {"hp": 110, "attack": 160, "defense": 110, "special_attack": 80, "special_defense": 110, "speed": 100},
            "groudon": {"hp": 100, "attack": 150, "defense": 140, "special_attack": 100, "special_defense": 90, "speed": 90},
            "rayquaza": {"hp": 105, "attack": 150, "defense": 90, "special_attack": 150, "special_defense": 90, "speed": 95},
            "kartana": {"hp": 59, "attack": 181, "defense": 131, "special_attack": 59, "special_defense": 31, "speed": 109},
            "pheromosa": {"hp": 71, "attack": 137, "defense": 37, "special_attack": 137, "special_defense": 37, "speed": 151},
            "aggron": {"hp": 70, "attack": 110, "defense": 180, "special_attack": 60, "special_defense": 60, "speed": 50},
            "rhyperior": {"hp": 115, "attack": 140, "defense": 130, "special_attack": 55, "special_defense": 55, "speed": 40},
            # Add one more Pokemon to get 5+ results for test
            "dragonite": {"hp": 91, "attack": 134, "defense": 95, "special_attack": 100, "special_defense": 100, "speed": 80},
        }

    def get_stat_spread_index(self) -> dict[str, Any]:
        """Returns stat spread quintiles for testing."""
        return {
            "STAT_MEDIANS": {
                "hp": 65,
                "attack": 75,
                "defense": 70,
                "special_attack": 72,
                "special_defense": 70,
                "speed": 65
            },
            "QUINTILES": {
                "D": {"hp": 50, "attack": 55, "defense": 50, "special_attack": 50, "special_defense": 50, "speed": 45},
                "C": {"hp": 65, "attack": 75, "defense": 70, "special_attack": 72, "special_defense": 70, "speed": 65},
                "B": {"hp": 80, "attack": 95, "defense": 85, "special_attack": 90, "special_defense": 85, "speed": 85},
                "A": {"hp": 95, "attack": 110, "defense": 100, "special_attack": 105, "special_defense": 100, "speed": 100},
                "S": {"hp": 255, "attack": 255, "defense": 255, "special_attack": 255, "special_defense": 255, "speed": 255}
            }
        }

    def get_type_matchup_index(self) -> dict[str, dict[str, frozenset[str]]]:
        """Returns type effectiveness matchups for testing - complete type chart."""
        return {
            "normal": {"double_damage_from": frozenset({"fighting"}), "half_damage_from": frozenset(), "no_damage_from": frozenset({"ghost"})},
            "fire": {"double_damage_from": frozenset({"water", "ground", "rock"}), "half_damage_from": frozenset({"fire", "grass", "ice", "bug", "steel", "fairy"}), "no_damage_from": frozenset()},
            "water": {"double_damage_from": frozenset({"electric", "grass"}), "half_damage_from": frozenset({"fire", "water", "ice", "steel"}), "no_damage_from": frozenset()},
            "electric": {"double_damage_from": frozenset({"ground"}), "half_damage_from": frozenset({"electric", "flying", "steel"}), "no_damage_from": frozenset()},
            "grass": {"double_damage_from": frozenset({"fire", "ice", "poison", "flying", "bug"}), "half_damage_from": frozenset({"water", "electric", "grass", "ground"}), "no_damage_from": frozenset()},
            "ice": {"double_damage_from": frozenset({"fire", "fighting", "rock", "steel"}), "half_damage_from": frozenset({"ice"}), "no_damage_from": frozenset()},
            "fighting": {"double_damage_from": frozenset({"flying", "psychic", "fairy"}), "half_damage_from": frozenset({"bug", "rock", "dark"}), "no_damage_from": frozenset()},
            "poison": {"double_damage_from": frozenset({"ground", "psychic"}), "half_damage_from": frozenset({"grass", "fighting", "poison", "bug", "fairy"}), "no_damage_from": frozenset()},
            "ground": {"double_damage_from": frozenset({"water", "grass", "ice"}), "half_damage_from": frozenset({"poison", "rock"}), "no_damage_from": frozenset({"electric"})},
            "flying": {"double_damage_from": frozenset({"electric", "ice", "rock"}), "half_damage_from": frozenset({"grass", "fighting", "bug"}), "no_damage_from": frozenset({"ground"})},
            "psychic": {"double_damage_from": frozenset({"bug", "ghost", "dark"}), "half_damage_from": frozenset({"fighting", "psychic"}), "no_damage_from": frozenset()},
            "bug": {"double_damage_from": frozenset({"fire", "flying", "rock"}), "half_damage_from": frozenset({"grass", "fighting", "ground"}), "no_damage_from": frozenset()},
            "rock": {"double_damage_from": frozenset({"water", "grass", "fighting", "ground", "steel"}), "half_damage_from": frozenset({"normal", "fire", "poison", "flying"}), "no_damage_from": frozenset()},
            "ghost": {"double_damage_from": frozenset({"ghost", "dark"}), "half_damage_from": frozenset({"bug", "poison"}), "no_damage_from": frozenset({"fighting", "normal"})},
            "dragon": {"double_damage_from": frozenset({"ice", "dragon", "fairy"}), "half_damage_from": frozenset({"fire", "water", "electric", "grass"}), "no_damage_from": frozenset()},
            "dark": {"double_damage_from": frozenset({"fighting", "bug", "fairy"}), "half_damage_from": frozenset({"ghost", "dark"}), "no_damage_from": frozenset({"psychic"})},
            "steel": {"double_damage_from": frozenset({"fire", "fighting", "ground"}), "half_damage_from": frozenset({"normal", "grass", "ice", "flying", "psychic", "bug", "rock", "dragon", "steel", "fairy"}), "no_damage_from": frozenset({"poison"})},
            "fairy": {"double_damage_from": frozenset({"poison", "steel"}), "half_damage_from": frozenset({"fighting", "bug", "dark"}), "no_damage_from": frozenset({"dragon"})},
        }
