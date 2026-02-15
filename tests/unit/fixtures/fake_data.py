"""
Small fake dataset for unit tests. No DB needed.
~29 Pokemon covering all test assertions in
test_candidate_finder.py and test_coverage_analyzer.py.
"""

# =============
# Pokemon Index
# =============
# {name: {display_name, number, height, weight, sprite_url,
#  description, genus, type_display, is_legendary,
#  is_mythical, is_ultra_beast}}


def _pokemon(
    display_name,
    number,
    type_display,
    is_legendary=False,
    is_mythical=False,
    is_ultra_beast=False,
):
    return {
        "display_name": display_name,
        "number": number,
        "height": 10,
        "weight": 100,
        "sprite_url": f"https://example.com/{number}.png",
        "description": f"A {display_name}.",
        "genus": "Pokemon",
        "type_display": type_display,
        "is_legendary": is_legendary,
        "is_mythical": is_mythical,
        "is_ultra_beast": is_ultra_beast,
    }


POKEMON_INDEX = {
    # Fire
    "charizard": _pokemon("Charizard", 6, "fire/flying"),
    "typhlosion": _pokemon("Typhlosion", 157, "fire"),
    "blaziken": _pokemon("Blaziken", 257, "fire/fighting"),
    "blacephalon": _pokemon(
        "Blacephalon",
        806,
        "fire/ghost",
        is_ultra_beast=True,
    ),
    # Psychic
    "alakazam": _pokemon("Alakazam", 65, "psychic"),
    "mewtwo": _pokemon("Mewtwo", 150, "psychic", is_legendary=True),
    "latias": _pokemon(
        "Latias",
        380,
        "dragon/psychic",
        is_legendary=True,
    ),
    "latios": _pokemon(
        "Latios",
        381,
        "dragon/psychic",
        is_legendary=True,
    ),
    "cresselia": _pokemon(
        "Cresselia",
        488,
        "psychic",
        is_legendary=True,
    ),
    "celebi": _pokemon(
        "Celebi",
        251,
        "psychic/grass",
        is_mythical=True,
    ),
    "jirachi": _pokemon(
        "Jirachi",
        385,
        "steel/psychic",
        is_mythical=True,
    ),
    "bronzong": _pokemon("Bronzong", 437, "steel/psychic"),
    "exeggutor": _pokemon("Exeggutor", 103, "grass/psychic"),
    "gallade": _pokemon("Gallade", 475, "psychic/fighting"),
    # Ghost
    "haunter": _pokemon("Haunter", 93, "ghost/poison"),
    # Normal
    "slaking": _pokemon("Slaking", 289, "normal"),
    "pidgeot": _pokemon("Pidgeot", 18, "normal/flying"),
    "regigigas": _pokemon(
        "Regigigas",
        486,
        "normal",
        is_legendary=True,
    ),
    # Dragon
    "dragapult": _pokemon("Dragapult", 887, "dragon/ghost"),
    "garchomp": _pokemon("Garchomp", 445, "dragon/ground"),
    "salamence": _pokemon("Salamence", 373, "dragon/flying"),
    "rayquaza": _pokemon(
        "Rayquaza",
        384,
        "dragon/flying",
        is_legendary=True,
    ),
    # Electric
    "pikachu": _pokemon("Pikachu", 25, "electric"),
    # Ground
    "groudon": _pokemon(
        "Groudon",
        383,
        "ground",
        is_legendary=True,
    ),
    # Rock/Steel
    "aggron": _pokemon("Aggron", 306, "steel/rock"),
    # Ground/Rock
    "rhyperior": _pokemon("Rhyperior", 464, "ground/rock"),
    # Ultra Beasts
    "nihilego": _pokemon(
        "Nihilego",
        793,
        "rock/poison",
        is_ultra_beast=True,
    ),
    "kartana": _pokemon(
        "Kartana",
        798,
        "grass/steel",
        is_ultra_beast=True,
    ),
    "pheromosa": _pokemon(
        "Pheromosa",
        795,
        "bug/fighting",
        is_ultra_beast=True,
    ),
    # Water (needed for coverage analyzer tests)
    "gyarados": _pokemon("Gyarados", 130, "water/flying"),
    # Dark (needed for coverage analyzer tests)
    "umbreon": _pokemon("Umbreon", 197, "dark"),
}


# ==========
# Move Index
# ==========
# {move_name: {pokemon_name: {learn_method: level/True}}}

MOVE_INDEX = {
    "hypnosis": {
        "bronzong": {"level-up": 20},
        "exeggutor": {"level-up": 1},
        "gallade": {"level-up": 1},
        "haunter": {"level-up": 1},
        "alakazam": {"level-up": 1},
    },
    "psychic": {
        "alakazam": {"level-up": 42},
        "bronzong": {"machine": True},
        "exeggutor": {"level-up": 37},
        "gallade": {"machine": True},
        "mewtwo": {"level-up": 1},
        "latias": {"level-up": 50},
        "latios": {"level-up": 50},
        "cresselia": {"level-up": 55},
        "celebi": {"level-up": 55},
        "jirachi": {"machine": True},
        "nihilego": {"machine": True},
        "blacephalon": {"machine": True},
    },
    "tackle": {
        "pikachu": {"level-up": 1},
        "pidgeot": {"level-up": 1},
        "slaking": {"level-up": 1},
        "typhlosion": {"level-up": 1},
        "aggron": {"level-up": 1},
        "rhyperior": {"level-up": 1},
    },
    "flamethrower": {
        "charizard": {"level-up": 54, "machine": True},
        "typhlosion": {"level-up": 43, "machine": True},
        "blaziken": {"machine": True},
        "blacephalon": {"machine": True},
    },
}


# ==========
# Stat Index
# ==========
# {pokemon_name: {hp, attack, defense, sp_atk, sp_def, speed}}

STAT_INDEX = {
    "charizard": {
        "hp": 78,
        "attack": 84,
        "defense": 78,
        "special_attack": 109,
        "special_defense": 85,
        "speed": 100,
    },
    "typhlosion": {
        "hp": 78,
        "attack": 84,
        "defense": 78,
        "special_attack": 109,
        "special_defense": 85,
        "speed": 100,
    },
    "blaziken": {
        "hp": 80,
        "attack": 120,
        "defense": 70,
        "special_attack": 110,
        "special_defense": 70,
        "speed": 80,
    },
    "blacephalon": {
        "hp": 53,
        "attack": 127,
        "defense": 53,
        "special_attack": 151,
        "special_defense": 79,
        "speed": 107,
    },
    "alakazam": {
        "hp": 55,
        "attack": 50,
        "defense": 45,
        "special_attack": 135,
        "special_defense": 95,
        "speed": 120,
    },
    "mewtwo": {
        "hp": 106,
        "attack": 110,
        "defense": 90,
        "special_attack": 154,
        "special_defense": 90,
        "speed": 130,
    },
    "latias": {
        "hp": 80,
        "attack": 80,
        "defense": 90,
        "special_attack": 110,
        "special_defense": 130,
        "speed": 110,
    },
    "latios": {
        "hp": 80,
        "attack": 90,
        "defense": 80,
        "special_attack": 130,
        "special_defense": 110,
        "speed": 110,
    },
    "cresselia": {
        "hp": 120,
        "attack": 70,
        "defense": 120,
        "special_attack": 75,
        "special_defense": 130,
        "speed": 85,
    },
    "celebi": {
        "hp": 100,
        "attack": 100,
        "defense": 100,
        "special_attack": 100,
        "special_defense": 100,
        "speed": 100,
    },
    "jirachi": {
        "hp": 100,
        "attack": 100,
        "defense": 100,
        "special_attack": 100,
        "special_defense": 100,
        "speed": 100,
    },
    "bronzong": {
        "hp": 67,
        "attack": 89,
        "defense": 116,
        "special_attack": 79,
        "special_defense": 116,
        "speed": 33,
    },
    "exeggutor": {
        "hp": 95,
        "attack": 95,
        "defense": 85,
        "special_attack": 125,
        "special_defense": 75,
        "speed": 55,
    },
    "gallade": {
        "hp": 68,
        "attack": 125,
        "defense": 65,
        "special_attack": 65,
        "special_defense": 115,
        "speed": 80,
    },
    "haunter": {
        "hp": 45,
        "attack": 50,
        "defense": 45,
        "special_attack": 115,
        "special_defense": 55,
        "speed": 95,
    },
    "slaking": {
        "hp": 150,
        "attack": 160,
        "defense": 100,
        "special_attack": 95,
        "special_defense": 65,
        "speed": 100,
    },
    "pidgeot": {
        "hp": 83,
        "attack": 80,
        "defense": 75,
        "special_attack": 70,
        "special_defense": 70,
        "speed": 101,
    },
    "regigigas": {
        "hp": 110,
        "attack": 160,
        "defense": 110,
        "special_attack": 80,
        "special_defense": 110,
        "speed": 100,
    },
    "dragapult": {
        "hp": 88,
        "attack": 120,
        "defense": 75,
        "special_attack": 100,
        "special_defense": 75,
        "speed": 142,
    },
    "garchomp": {
        "hp": 108,
        "attack": 130,
        "defense": 95,
        "special_attack": 80,
        "special_defense": 85,
        "speed": 102,
    },
    "salamence": {
        "hp": 95,
        "attack": 135,
        "defense": 80,
        "special_attack": 110,
        "special_defense": 80,
        "speed": 100,
    },
    "rayquaza": {
        "hp": 105,
        "attack": 150,
        "defense": 90,
        "special_attack": 150,
        "special_defense": 90,
        "speed": 95,
    },
    "pikachu": {
        "hp": 35,
        "attack": 55,
        "defense": 40,
        "special_attack": 50,
        "special_defense": 50,
        "speed": 90,
    },
    "groudon": {
        "hp": 100,
        "attack": 150,
        "defense": 140,
        "special_attack": 100,
        "special_defense": 90,
        "speed": 95,
    },
    "aggron": {
        "hp": 70,
        "attack": 110,
        "defense": 180,
        "special_attack": 60,
        "special_defense": 60,
        "speed": 50,
    },
    "rhyperior": {
        "hp": 115,
        "attack": 140,
        "defense": 130,
        "special_attack": 55,
        "special_defense": 55,
        "speed": 40,
    },
    "nihilego": {
        "hp": 109,
        "attack": 53,
        "defense": 47,
        "special_attack": 127,
        "special_defense": 131,
        "speed": 103,
    },
    "kartana": {
        "hp": 59,
        "attack": 181,
        "defense": 131,
        "special_attack": 59,
        "special_defense": 31,
        "speed": 109,
    },
    "pheromosa": {
        "hp": 71,
        "attack": 137,
        "defense": 37,
        "special_attack": 137,
        "special_defense": 37,
        "speed": 151,
    },
    "gyarados": {
        "hp": 95,
        "attack": 125,
        "defense": 79,
        "special_attack": 60,
        "special_defense": 100,
        "speed": 81,
    },
    "umbreon": {
        "hp": 95,
        "attack": 65,
        "defense": 110,
        "special_attack": 60,
        "special_defense": 130,
        "speed": 65,
    },
}


# =================
# Stat Spread Index
# =================
# Approximate medians and quintiles for the fake dataset

STAT_SPREAD_INDEX = {
    "STAT_MEDIANS": {
        "hp": 80,
        "attack": 100,
        "defense": 80,
        "special_attack": 100,
        "special_defense": 85,
        "speed": 95,
    },
    "QUINTILES": {
        "hp": {
            "20th": 55,
            "40th": 70,
            "60th": 95,
            "80th": 108,
            "100th": 150,
        },
        "attack": {
            "20th": 55,
            "40th": 84,
            "60th": 120,
            "80th": 140,
            "100th": 181,
        },
        "defense": {
            "20th": 45,
            "40th": 75,
            "60th": 90,
            "80th": 120,
            "100th": 180,
        },
        "special_attack": {
            "20th": 60,
            "40th": 80,
            "60th": 109,
            "80th": 130,
            "100th": 154,
        },
        "special_defense": {
            "20th": 55,
            "40th": 75,
            "60th": 90,
            "80th": 115,
            "100th": 131,
        },
        "speed": {
            "20th": 50,
            "40th": 80,
            "60th": 100,
            "80th": 109,
            "100th": 151,
        },
    },
}


# ==========
# Type Index
# ==========
# {type_name: frozenset(pokemon_names)}
# Dual-type Pokemon appear under BOTH types


def _build_type_index(pokemon_index):
    type_index = {}
    for name, data in pokemon_index.items():
        types = data["type_display"].split("/")
        for t in types:
            if t not in type_index:
                type_index[t] = set()
            type_index[t].add(name)
    return {t: frozenset(names) for t, names in type_index.items()}


TYPE_INDEX = _build_type_index(POKEMON_INDEX)


# ==================
# Machine Moves Index
# ==================

MACHINE_MOVES_INDEX = {
    "flamethrower": "TM35",
    "psychic": "TM29",
}


# =================
# Type Matchup Data
# =================
# Full 18x18 type chart.
# Stored as {defender: {attacker: multiplier}}.
# Only non-1x entries are stored; missing = 1x.

_TYPE_CHART_OVERRIDES = {
    "normal": {
        "fighting": 2.0,
        "ghost": 0.0,
    },
    "fire": {
        "water": 2.0,
        "ground": 2.0,
        "rock": 2.0,
        "fire": 0.5,
        "grass": 0.5,
        "ice": 0.5,
        "bug": 0.5,
        "steel": 0.5,
        "fairy": 0.5,
    },
    "water": {
        "electric": 2.0,
        "grass": 2.0,
        "fire": 0.5,
        "water": 0.5,
        "ice": 0.5,
        "steel": 0.5,
    },
    "electric": {
        "ground": 2.0,
        "electric": 0.5,
        "flying": 0.5,
        "steel": 0.5,
    },
    "grass": {
        "fire": 2.0,
        "ice": 2.0,
        "poison": 2.0,
        "flying": 2.0,
        "bug": 2.0,
        "water": 0.5,
        "electric": 0.5,
        "grass": 0.5,
        "ground": 0.5,
    },
    "ice": {
        "fire": 2.0,
        "fighting": 2.0,
        "rock": 2.0,
        "steel": 2.0,
        "ice": 0.5,
    },
    "fighting": {
        "flying": 2.0,
        "psychic": 2.0,
        "fairy": 2.0,
        "bug": 0.5,
        "rock": 0.5,
        "dark": 0.5,
    },
    "poison": {
        "ground": 2.0,
        "psychic": 2.0,
        "fighting": 0.5,
        "poison": 0.5,
        "bug": 0.5,
        "grass": 0.5,
        "fairy": 0.5,
    },
    "ground": {
        "water": 2.0,
        "grass": 2.0,
        "ice": 2.0,
        "electric": 0.0,
        "poison": 0.5,
        "rock": 0.5,
    },
    "flying": {
        "electric": 2.0,
        "ice": 2.0,
        "rock": 2.0,
        "ground": 0.0,
        "fighting": 0.5,
        "bug": 0.5,
        "grass": 0.5,
    },
    "psychic": {
        "bug": 2.0,
        "ghost": 2.0,
        "dark": 2.0,
        "fighting": 0.5,
        "psychic": 0.5,
    },
    "bug": {
        "fire": 2.0,
        "flying": 2.0,
        "rock": 2.0,
        "fighting": 0.5,
        "ground": 0.5,
        "grass": 0.5,
    },
    "rock": {
        "water": 2.0,
        "grass": 2.0,
        "fighting": 2.0,
        "ground": 2.0,
        "steel": 2.0,
        "normal": 0.5,
        "fire": 0.5,
        "poison": 0.5,
        "flying": 0.5,
    },
    "ghost": {
        "ghost": 2.0,
        "dark": 2.0,
        "normal": 0.0,
        "fighting": 0.0,
        "poison": 0.5,
        "bug": 0.5,
    },
    "dragon": {
        "ice": 2.0,
        "dragon": 2.0,
        "fairy": 2.0,
        "fire": 0.5,
        "water": 0.5,
        "electric": 0.5,
        "grass": 0.5,
    },
    "dark": {
        "fighting": 2.0,
        "bug": 2.0,
        "fairy": 2.0,
        "ghost": 0.5,
        "dark": 0.5,
        "psychic": 0.0,
    },
    "steel": {
        "fire": 2.0,
        "fighting": 2.0,
        "ground": 2.0,
        "normal": 0.5,
        "grass": 0.5,
        "ice": 0.5,
        "flying": 0.5,
        "psychic": 0.5,
        "bug": 0.5,
        "rock": 0.5,
        "dragon": 0.5,
        "steel": 0.5,
        "fairy": 0.5,
        "poison": 0.0,
    },
    "fairy": {
        "poison": 2.0,
        "steel": 2.0,
        "fighting": 0.5,
        "bug": 0.5,
        "dark": 0.5,
        "dragon": 0.0,
    },
}

ALL_TYPES = frozenset(_TYPE_CHART_OVERRIDES.keys())


def _get_base_multiplier(defender: str, attacker: str) -> float:
    overrides = _TYPE_CHART_OVERRIDES.get(defender)
    if overrides and attacker in overrides:
        return overrides[attacker]
    return 1.0


# ========================
# Type Pairs (dual types)
# ========================
# Canonical pairs for Pokemon in our fake dataset


def _build_type_pairs(pokemon_index):
    pairs = set()
    for data in pokemon_index.values():
        types = data["type_display"].split("/")
        if len(types) == 2:
            pairs.add(f"{types[0]}/{types[1]}")
    return frozenset(pairs)


TYPE_PAIRS = _build_type_pairs(POKEMON_INDEX)


# ==============================
# Opponent Weakness Type Index
# ==============================
# {defending_type_or_combo:
#  {"4x": frozenset(attackers), "2x": ..., etc.}}


def _classify_multiplier(eff, mult, value):
    if mult == 4.0:
        eff["4x"].append(value)
    elif mult == 2.0:
        eff["2x"].append(value)
    elif mult == 1.0:
        eff["1x"].append(value)
    elif mult == 0.5:
        eff["0.5x"].append(value)
    elif mult == 0.25:
        eff["0.25x"].append(value)
    elif mult == 0.0:
        eff["0x"].append(value)


def _calc_defensive_effectiveness(
    defending_types: list[str],
) -> dict[str, frozenset[str]]:
    eff = {"4x": [], "2x": [], "1x": [], "0.5x": [], "0.25x": [], "0x": []}
    for attacker in ALL_TYPES:
        mult = 1.0
        for defender in defending_types:
            mult *= _get_base_multiplier(defender, attacker)
        _classify_multiplier(eff, mult, attacker)
    return {k: frozenset(v) for k, v in eff.items()}


def _build_opponent_weakness_index(type_pairs):
    index = {}
    for t in ALL_TYPES:
        index[t] = _calc_defensive_effectiveness([t])
    for pair in type_pairs:
        t1, t2 = pair.split("/")
        index[pair] = _calc_defensive_effectiveness([t1, t2])
    return index


OPPONENT_WEAKNESS_TYPE_INDEX = _build_opponent_weakness_index(TYPE_PAIRS)


# ==============================
# My Team Strengths Type Index
# ==============================
# {attacking_type_or_combo:
#  {"4x": frozenset(defending_types_or_combos), ...}}


def _calc_offensive_effectiveness(
    attacking_types: list[str],
    all_pairs: frozenset[str],
) -> dict[str, frozenset[str]]:
    eff = {"4x": [], "2x": [], "1x": [], "0.5x": [], "0.25x": [], "0x": []}

    # Against single types
    for defender in ALL_TYPES:
        mult = 1.0
        for attacker in attacking_types:
            mult *= _get_base_multiplier(defender, attacker)
        _classify_multiplier(eff, mult, defender)

    # Against dual types
    for pair in all_pairs:
        d1, d2 = pair.split("/")
        mult = 1.0
        for attacker in attacking_types:
            mult *= _get_base_multiplier(d1, attacker)
            mult *= _get_base_multiplier(d2, attacker)
        _classify_multiplier(eff, mult, pair)

    return {k: frozenset(v) for k, v in eff.items()}


def _build_my_team_strengths_index(type_pairs):
    index = {}
    for t in ALL_TYPES:
        index[t] = _calc_offensive_effectiveness([t], type_pairs)
    for pair in type_pairs:
        t1, t2 = pair.split("/")
        index[pair] = _calc_offensive_effectiveness([t1, t2], type_pairs)
    return index


MY_TEAM_STRENGTHS_TYPE_INDEX = _build_my_team_strengths_index(TYPE_PAIRS)
