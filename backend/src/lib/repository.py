import json
from typing import Any

import structlog

from backend.src.config.settings import settings

# DTOs
from backend.src.lib.dtos import Pokemon, PokemonMove, PokemonStats, PokemonType, StatSpread, Tm, TypeMatchup

# Exceptions
from backend.src.lib.exceptions import (
    InvalidPokemonMoveError,
    InvalidPokemonStatError,
    InvalidPokemonTypeError,
    NoPokemonFoundError,
    TooManyTypesError,
)

# Stat ranking weights (easily adjustable)
STAT_WEIGHT_PRIMARY = 0.7
STAT_WEIGHT_SECONDARY = 0.3

logger = structlog.get_logger(__name__)


class JSONRepository:
    def __init__(self):
        self._load_all_indexes()

    def _load_all_indexes(self):
        """Load all indexes from database on initialization."""
        # Load canonical type pairs
        with open(settings.type_pairs_fixture_path) as f:
            type_pairs_data = json.load(f)
            self.type_pairs = frozenset(type_pairs_data["type_pairs"])

        try:
            self._pokemon_index = self._load_pokemon_index()
            self._move_index = self._load_move_index()
            self._stat_index = self._load_stat_index()
            self._stat_spread_index = self._load_stat_spread_index()
            self._type_index = self._load_type_index()
            self._opponent_weakness_type_index = self._load_opponent_weakness_type_index()
            self._my_team_strengths_type_index = self._load_my_team_strengths_type_index()
            self._machine_moves_index = self._load_machine_moves_index()
        except (OSError, ValueError) as e:
            logger.error("Failed to load indexes from fixtures", error=str(e))
            raise

        logger.info(
            "All indexes loaded successfully",
            pokemon_count=len(self._pokemon_index),
            move_count=len(self._move_index),
            stat_count=len(self._stat_index),
            stat_spread_count=len(self._stat_spread_index),
            type_count=len(self._type_index),
            opponent_weakness_count=len(self._opponent_weakness_type_index),
            my_team_strengths_count=len(self._my_team_strengths_type_index),
            machine_moves_count=len(self._machine_moves_index),
        )

    # Pokemon
    def _load_pokemon_index(self) -> dict[str, dict]:

        with open(settings.pokemon_fixture_path) as file:
            data = json.load(file)

        rows = [Pokemon(**entry) for entry in data]
        pokemon_index = {row.name: row.model_dump() for row in rows}

        logger.info("Pokemon info index created successfully", pokemon_count=len(pokemon_index))
        return pokemon_index

    # Moves
    def _load_move_index(self) -> dict[str, dict[str, dict[str, Any]]]:

        with open(settings.pokemon_move_fixture_path) as file:
            data = json.load(file)

        rows = [PokemonMove(**listing) for listing in data]

        move_index = {}

        for row in rows:
            if row.move_name not in move_index:
                move_index[row.move_name] = {}
            if row.pokemon_name not in move_index[row.move_name]:
                move_index[row.move_name][row.pokemon_name] = {}
            if row.learn_method == "level-up":
                move_index[row.move_name][row.pokemon_name][row.learn_method] = row.level
            else:
                move_index[row.move_name][row.pokemon_name][row.learn_method] = True

        logger.info("Move index created successfully", move_count=len(move_index))
        return move_index

    def _load_stat_index(self) -> dict[str, dict[str, int]]:

        with open(settings.pokemon_stats_fixture_path) as file:
            data = json.load(file)

        rows = [PokemonStats(**listing) for listing in data]

        stat_index = {}
        for row in rows:
            stat_index[row.pokemon_name] = {
                "hp": row.hp,
                "attack": row.attack,
                "defense": row.defense,
                "special_attack": row.special_attack,
                "special_defense": row.special_defense,
                "speed": row.speed,
            }

        logger.info("Stat index created successfully", stat_count=len(stat_index))
        return stat_index

    def _load_stat_spread_index(self) -> dict[str, Any]:

        with open(settings.stat_spreads_fixture_path) as file:
            data = json.load(file)

        rows = [StatSpread(**listing) for listing in data]

        medians = {}
        quintiles = {}
        for row in rows:
            stat_name = row.stat_name

            # Store median
            medians[stat_name] = row.median

            # Store quintiles
            quintiles[stat_name] = {
                "20th": row.percentile_20,
                "40th": row.percentile_40,
                "60th": row.percentile_60,
                "80th": row.percentile_80,
                "100th": row.percentile_100,
            }

        logger.info("Stat spread index created successfully")  # No need for count here.
        return {"STAT_MEDIANS": medians, "QUINTILES": quintiles}

    def _load_type_index(self) -> dict[str, frozenset[str]]:
        """Load type index: {type_name: frozenset(pokemon_names)}

        Dual-type Pokemon are stored under BOTH of their individual types.
        For example, Charizard (fire/flying) appears in both type_index["fire"]
        and type_index["flying"] for easy searching.
        """
        with open(settings.pokemon_type_fixture_path) as file:
            data = json.load(file)

        rows = [PokemonType(**listing) for listing in data]

        type_index = {}

        for row in rows:
            if row.type_name not in type_index:
                type_index[row.type_name] = []
            type_index[row.type_name].append(row.pokemon_name)

        # Convert lists to frozensets
        filtered = {type_name: frozenset(pokemon_list) for type_name, pokemon_list in type_index.items()}

        logger.info("Type index created successfully", type_count=len(filtered))
        return filtered

    def _load_opponent_weakness_type_index(self) -> dict[str, dict[str, frozenset[str]]]:
        """Opponent weakness index: What attacks this defending type effectively.

        Returns: {defending_type: {"4x": frozenset(attacking_types), ...}}
        """
        with open(settings.type_matchups_fixture_path) as file:
            data = json.load(file)

        rows = [TypeMatchup(**listing) for listing in data]

        # Build base matchup lookup
        base_matchups = {}
        all_types = set()
        for row in rows:
            defender, attacker, multiplier = row.defender_type, row.attacker_type, row.multiplier
            all_types.add(defender)
            all_types.add(attacker)
            if defender not in base_matchups:
                base_matchups[defender] = {}
            base_matchups[defender][attacker] = multiplier

        opponent_weakness_index = {}

        # Single-type defenses
        for defender_type in all_types:
            opponent_weakness_index[defender_type] = self._calculate_my_teams_effectiveness(
                base_matchups, all_types, [defender_type]
            )

        # Dual-type defenses
        for type_pair in self.type_pairs:
            type1, type2 = type_pair.split("/")
            opponent_weakness_index[type_pair] = self._calculate_my_teams_effectiveness(
                base_matchups, all_types, [type1, type2]
            )

        logger.info(
            "Opponent weakness type index created",
            single_types=sum(1 for k in opponent_weakness_index if "/" not in k),
            dual_types=sum(1 for k in opponent_weakness_index if "/" in k),
        )
        return opponent_weakness_index

    def _load_my_team_strengths_type_index(self) -> dict[str, dict[str, frozenset[str]]]:
        """My team strengths index: What defending types this attacking type is effective against.

        Returns: {attacking_type: {"4x": frozenset(defending_types), ...}}
        """
        with open(settings.type_matchups_fixture_path) as file:
            data = json.load(file)

        rows = [TypeMatchup(**listing) for listing in data]

        base_matchups = {}
        all_types = set()
        for row in rows:
            defender, attacker, multiplier = row.defender_type, row.attacker_type, row.multiplier
            all_types.add(defender)
            all_types.add(attacker)
            if defender not in base_matchups:
                base_matchups[defender] = {}
            base_matchups[defender][attacker] = multiplier

        my_team_strengths_index = {}

        # Single-type attackers
        for attack_type in all_types:
            my_team_strengths_index[attack_type] = self._calculate_enemy_effectiveness(
                base_matchups, all_types, self.type_pairs, [attack_type]
            )

        # Dual-type attackers
        for type_pair in self.type_pairs:
            type1, type2 = type_pair.split("/")
            my_team_strengths_index[type_pair] = self._calculate_enemy_effectiveness(
                base_matchups, all_types, self.type_pairs, [type1, type2]
            )

        logger.info(
            "My team strengths type index created",
            single_types=sum(1 for k in my_team_strengths_index if "/" not in k),
            dual_types=sum(1 for k in my_team_strengths_index if "/" in k),
        )
        return my_team_strengths_index

    def _load_machine_moves_index(self) -> dict:
        """Load machine moves index: {move_name: machine_id}"""
        with open(settings.tm_fixture_path) as file:
            data = json.load(file)

        rows = [Tm(**listing) for listing in data]

        machine_moves_index = {}
        for row in rows:
            if row.machine_id is not None:
                machine_moves_index[row.name] = row.machine_id

        logger.info("Machine moves index created successfully", machine_moves_count=len(machine_moves_index))
        return machine_moves_index

    def _calculate_my_teams_effectiveness(
        self, base_matchups: dict, all_types: set, defending_types: list
    ) -> dict[str, frozenset[str]]:
        """Calculate what attacks this defending type effectively."""
        eff = {"4x": [], "2x": [], "1x": [], "0.5x": [], "0.25x": [], "0x": []}

        for attacker in all_types:
            mult = 1.0
            for defender in defending_types:
                if defender in base_matchups and attacker in base_matchups[defender]:
                    mult *= base_matchups[defender][attacker]

            if mult == 4.0:
                eff["4x"].append(attacker)
            elif mult == 2.0:
                eff["2x"].append(attacker)
            elif mult == 1.0:
                eff["1x"].append(attacker)
            elif mult == 0.5:
                eff["0.5x"].append(attacker)
            elif mult == 0.25:
                eff["0.25x"].append(attacker)
            elif mult == 0.0:
                eff["0x"].append(attacker)

        return {k: frozenset(v) for k, v in eff.items()}

    def _calculate_enemy_effectiveness(
        self, base_matchups: dict, all_types: set, all_pairs: frozenset, attacking_types: list
    ) -> dict[str, frozenset[str]]:
        """Calculate what this attacking type is effective against."""
        eff = {"4x": [], "2x": [], "1x": [], "0.5x": [], "0.25x": [], "0x": []}

        # Against single types
        for defender in all_types:
            mult = 1.0
            for attacker in attacking_types:
                if defender in base_matchups and attacker in base_matchups[defender]:
                    mult *= base_matchups[defender][attacker]

            if mult == 4.0:
                eff["4x"].append(defender)
            elif mult == 2.0:
                eff["2x"].append(defender)
            elif mult == 1.0:
                eff["1x"].append(defender)
            elif mult == 0.5:
                eff["0.5x"].append(defender)
            elif mult == 0.25:
                eff["0.25x"].append(defender)
            elif mult == 0.0:
                eff["0x"].append(defender)

        # Against dual types
        for type_pair in all_pairs:
            def1, def2 = type_pair.split("/")
            mult = 1.0
            for attacker in attacking_types:
                if def1 in base_matchups and attacker in base_matchups[def1]:
                    mult *= base_matchups[def1][attacker]
                if def2 in base_matchups and attacker in base_matchups[def2]:
                    mult *= base_matchups[def2][attacker]

            if mult == 4.0:
                eff["4x"].append(type_pair)
            elif mult == 2.0:
                eff["2x"].append(type_pair)
            elif mult == 1.0:
                eff["1x"].append(type_pair)
            elif mult == 0.5:
                eff["0.5x"].append(type_pair)
            elif mult == 0.25:
                eff["0.25x"].append(type_pair)
            elif mult == 0.0:
                eff["0x"].append(type_pair)

        return {k: frozenset(v) for k, v in eff.items()}

    # Public interface - return cached indexes
    def get_pokemon_index(self) -> dict[str, dict[str, Any]]:
        return self._pokemon_index

    def get_move_index(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Returns move index: {move_name: {pokemon_name: {learn_method: data}}}"""
        return self._move_index

    def get_stat_index(self) -> dict[str, dict[str, int]]:
        """Returns base stats: {pokemon_name: {stat_name: value}}"""
        return self._stat_index

    def get_stat_spread_index(self) -> dict[str, Any]:
        """Returns stat quintiles: {category: {stat_name: value}}"""
        return self._stat_spread_index

    def get_type_index(self) -> dict[str, frozenset[str]]:
        """Returns type index: {type_name: frozenset(pokemon_names)}"""
        return self._type_index

    def get_opponent_weakness_type_index(self) -> dict[str, dict[str, frozenset[str]]]:
        """Returns opponent weakness index: {defending_type: {"4x": frozenset(attacking_types), ...}}"""
        return self._opponent_weakness_type_index

    def get_my_team_strengths_type_index(self) -> dict[str, dict[str, frozenset[str]]]:
        """Returns my team strengths index: {attacking_type: {"4x": frozenset(defending_types), ...}}"""
        return self._my_team_strengths_type_index

    def get_machine_moves_index(self) -> dict:
        return self._machine_moves_index

    def get_pokemon_by_name(self, name: str) -> dict[str, Any]:

        # logger.debug(
        #     "Searching pokemon by name",
        #     name=name
        #     )

        # Validation

        # Case 2: Empty string
        if not name:
            raise ValueError("Pokemon name must be provided")

        # Case 3: Name does not exist
        if name not in self._pokemon_index:
            raise InvalidPokemonMoveError(f"Invalid name: '{name}'")

        # Case 4: Success
        results = self._pokemon_index[name]

        # logger.info("Found pokemon by name", name=name)
        return results

    def get_pokemon_by_move(
        self,
        move: str,
        include_mythical: bool = False,
        include_legendary: bool = False,
        include_ultra_beasts: bool = False,
    ) -> dict[str, dict[str, Any]]:

        # logger.debug(
        #     "Searching pokemon by move",
        #     move=move,
        #     include_mythical=include_mythical,
        #     include_legendary=include_legendary,
        #     include_ultra_beasts=include_ultra_beasts
        #     )

        # Validation
        # Case 1: Invalid argument datatype
        if not isinstance(move, str):
            raise TypeError(f"Expected str, got {type(move).__name__}: {move!r}")

        # Case 2: Empty string
        if not move:
            raise ValueError("Move name must be provided")

        # Case 3: Move does not exist
        if move not in self._move_index:
            raise InvalidPokemonMoveError(f"Invalid move: '{move.replace('_', ' ')}'")

        # Case 4: Success
        pokemon_found = self._move_index[move]

        # Filter by species status
        filtered = {
            name: info
            for name, info in pokemon_found.items()
            if (include_legendary or not self._pokemon_index[name]["is_legendary"])
            and (include_mythical or not self._pokemon_index[name]["is_mythical"])
            and (include_ultra_beasts or not self._pokemon_index[name]["is_ultra_beast"])
        }

        logger.info("Found pokemon by move", move=move, count=len(filtered))
        return filtered

    def get_pokemon_by_stats(
        self,
        primary_stat: str,
        secondary_stat: str,
        min_primary: int = 0,
        min_secondary: int | None = None,
        min_speed: int | None = None,
        include_legendary: bool = False,
        include_mythical: bool = False,
        include_ultra_beasts: bool = False,
    ) -> dict[str, dict]:

        # logger.debug(
        #     "Searching pokemon by stats",
        #     primary_stat=primary_stat,
        #     secondary_stat=secondary_stat,
        #     min_primary=min_primary,
        #     min_secondary=min_secondary,
        #     min_speed=min_speed,
        #     include_legendary=include_legendary,
        #     include_mythical=include_mythical,
        #     include_ultra_beasts=include_ultra_beasts
        #     )

        # Case 2: Empty stat names (Caller mistake)
        if not primary_stat:
            raise InvalidPokemonStatError("primary_stat cannot be empty")

        if not secondary_stat:
            raise InvalidPokemonStatError("secondary_stat cannot be empty")

        # Case 3: Invalid stat names (Caller mistake)
        valid_stats = {"hp", "attack", "defense", "special_attack", "special_defense", "speed"}

        if primary_stat not in valid_stats:
            raise InvalidPokemonStatError(f"Invalid primary_stat: '{primary_stat}'. Valid stats: {sorted(valid_stats)}")

        if secondary_stat not in valid_stats:
            raise InvalidPokemonStatError(
                f"Invalid secondary_stat: '{secondary_stat}'. Valid stats: {sorted(valid_stats)}"
            )

        # Case 4: Default min_secondary to median if not provided
        if min_secondary is None:
            min_secondary = int(self._stat_spread_index["STAT_MEDIANS"][secondary_stat])

        # Case 5: Filter by legendary/mythical/ultra beast status first (optimization)
        # Only include Pokemon that exist in both indices
        filtered_by_species = {
            name: stats
            for name, stats in self._stat_index.items()
            if name in self._pokemon_index
            and (include_legendary or not self._pokemon_index[name]["is_legendary"])
            and (include_mythical or not self._pokemon_index[name]["is_mythical"])
            and (include_ultra_beasts or not self._pokemon_index[name]["is_ultra_beast"])
        }

        # Case 6: Filter by stat thresholds (including optional speed filter)
        candidates = {
            name: stats
            for name, stats in filtered_by_species.items()
            if stats[primary_stat] >= min_primary
            and stats[secondary_stat] >= min_secondary
            and (min_speed is None or stats["speed"] >= min_speed)
        }

        # Case 7: No Pokemon found matching criteria
        if not candidates:
            raise NoPokemonFoundError(
                f"No Pokemon found: {primary_stat} {min_primary} and {secondary_stat} {min_secondary}"
            )

        # Case 8: Rank by weighted composite score (70% primary, 30% secondary)
        # Higher score = better
        ranked = sorted(
            candidates.items(),
            key=lambda x: STAT_WEIGHT_PRIMARY * x[1][primary_stat] + STAT_WEIGHT_SECONDARY * x[1][secondary_stat],
            reverse=True,  # Best first
        )

        logger.info(
            "Found pokemon by stats",
            primary_stat=primary_stat,
            secondary_stat=secondary_stat,
            min_primary=min_primary,
            min_secondary=min_secondary,
            min_speed=min_speed,
            include_legendary=include_legendary,
            include_mythical=include_mythical,
            include_ultra_beasts=include_ultra_beasts,
            count=len(ranked),
        )

        # Return just the names, in ranked order
        return {name: stats for name, stats in ranked}

    def validate_pokemon_types(self, *types: str) -> None:
        """Validate that all provided types are real Pokemon types.
        Raises InvalidPokemonTypeError if any are invalid.
        """
        invalid_types = [t for t in types if t not in self._type_index]
        if invalid_types:
            raise InvalidPokemonTypeError(
                f"Invalid Pokemon type(s): {invalid_types}. Valid types: {sorted(self._type_index.keys())}"
            )

    def get_pokemon_by_type(
        self,
        *types: str,
        include_legendary: bool = False,
        include_mythical: bool = False,
        include_ultra_beasts: bool = False,
    ) -> frozenset[str]:

        # logger.debug(
        #     "Searching pokemon by type",
        #     types=types,
        #     include_legendary=include_legendary,
        #     include_mythical=include_mythical,
        #     include_ultra_beasts=include_ultra_beasts
        #     )

        # Case 1: Incorrect arg datatype (Programmer mistake)
        for t in types:
            if not isinstance(t, str):
                raise TypeError(f"Expected str, got {type(t).__name__}: {t!r}")

        # Case 2: No pokemon type provided (Caller mistake)
        if not types:
            raise ValueError("At least one Pokemon type must be provided")

        # Case 3: Too many args (Caller mistake)
        if len(types) > 2:
            raise TooManyTypesError(f"Maximum 2 types allowed, got {len(types)}: {types}")

        # Case 4: One or more invalid pokemon types (Caller mistake)
        invalid_types = [t for t in types if t not in self._type_index]
        if invalid_types:
            raise InvalidPokemonTypeError(
                f"Invalid Pokemon type(s): {invalid_types}. Valid types: {sorted(self._type_index.keys())}"
            )

        # Case 5 & 6: Single or dual type search
        pokemon_list = self._type_index[types[0]]  # type: ignore
        for t in types[1:]:
            pokemon_list &= self._type_index[t]

        # Case 7: No pokemon found (This might be valid, not always an error)
        if not pokemon_list:
            raise NoPokemonFoundError(f"No Pokemon found with type(s): {types}")

        # Case 8: Filter by legendary/mythical/ultra beast status
        filtered = frozenset(
            name
            for name in pokemon_list
            if (include_legendary or not self._pokemon_index[name]["is_legendary"])
            and (include_mythical or not self._pokemon_index[name]["is_mythical"])
            and (include_ultra_beasts or not self._pokemon_index[name]["is_ultra_beast"])
        )

        if not filtered:
            raise NoPokemonFoundError(f"No Pokemon found with type(s) {types} after filtering legendary/mythical")

        logger.info(
            "Found pokemon by type",
            types=types,
            include_legendary=include_legendary,
            include_mythical=include_mythical,
            include_ultra_beasts=include_ultra_beasts,
            count=len(filtered),
        )

        return filtered

    def get_type_effectiveness(self, *types: str) -> dict[str, frozenset[str]]:
        # logger.debug(
        #     "Searching type matchups",
        #     types=types
        # )

        # Validation

        # Case 2: No arguments provided
        if not types:
            raise ValueError("At least one Pokemon type must be provided")

        # Case 3: Too many arguments provided
        if len(types) > 2:
            raise TooManyTypesError(f"Maximum 2 types allowed, got {len(types)}: {types}")

        # Build the lookup key
        if len(types) == 1:
            lookup_key = types[0]  # type: ignore[misc]
        else:
            # Dual-type: normalize to canonical ordering
            type_pair = f"{types[0]}/{types[1]}"  # type: ignore[misc]
            reverse_pair = f"{types[1]}/{types[0]}"  # type: ignore[misc]

            # Check which ordering exists in the index
            if type_pair in self._opponent_weakness_type_index:
                lookup_key = type_pair
            elif reverse_pair in self._opponent_weakness_type_index:
                lookup_key = reverse_pair
            else:
                # Neither ordering exists - invalid type combination
                raise InvalidPokemonTypeError(
                    f"Invalid type combination: {types}. "
                    f"Valid types: {sorted([k for k in self._opponent_weakness_type_index.keys() if '/' not in k])}"
                )

        # Validate the lookup key exists
        if lookup_key not in self._opponent_weakness_type_index:
            raise InvalidPokemonTypeError(
                f"Invalid type: {lookup_key}. "
                f"Valid types: {sorted([k for k in self._opponent_weakness_type_index.keys() if '/' not in k])}"
            )

        # Simple O(1) lookup instead of O(n) calculation
        result = self._opponent_weakness_type_index[lookup_key]

        logger.info("Found type matchups", types=types, lookup_key=lookup_key, count=len(result))

        return result
