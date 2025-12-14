# Imports
import structlog

from typing import Any
from collections import defaultdict

from backend.src.lib.repository import SQLAlchemyRepository

# Exceptions
from backend.src.lib.exceptions import (
    InvalidPokemonMoveError,
    InvalidPokemonNameError,
    InvalidPokemonTypeError,
    NoPokemonFoundError,
    TooManyTypesError,
)

# Stat ranking weights (easily adjustable)
STAT_WEIGHT_PRIMARY = 0.7
STAT_WEIGHT_SECONDARY = 0.3

logger = structlog.get_logger(__name__)

# Class
class CandidateFinderService():

    # Initialize
    def __init__(self, repository: SQLAlchemyRepository):
        self.repository = repository
        if not self.repository:
            logger.error("Repository not loaded properly")
            raise ValueError("Repository returned empty REPOSITORY object")
                
        self._pokemon_index = self.repository.get_pokemon_index()
        if not self._pokemon_index:
            logger.error("Empty pokemon index")
            raise ValueError("Repository returned empty POKEMON index")

        
        self._move_index = self.repository.get_move_index()
        if not self._move_index:
            logger.error("Empty move index")
            raise ValueError("Repository returned empty MOVE index")

        self._stat_spreads_index = self.repository.get_stat_spread_index()
        if not self._stat_spreads_index:
            logger.error("Empty stat spreads index")
            raise ValueError("Repository returned empty STAT SPREADS index")

        self._stat_index = self.repository.get_stat_index()
        if not self._stat_index:
            logger.error("Empty stats index")
            raise ValueError("Repository returned empty STAT index")

        self._type_index = self.repository.get_type_index()
        if not self._type_index:
            logger.error("Empty type index")
            raise ValueError("Repository returned empty TYPE index")

        self._type_matchup_index = self.repository.get_type_matchup_index()
        if not self._type_matchup_index:
            logger.error("Empty type_matchup_index")
            raise ValueError("Repository returned empty TYPE_MATCHUP index")
        
    def get_pokemon_by_name(
        self,
        name: str
    ) -> dict[str, Any]:
        
        logger.debug(
            "Searching pokemon by name", 
            name=name
            )
        
        # Validation
        # Case 1: Invalid argument datatype
        if not isinstance(name, str):
            raise TypeError(f"Expected str, got {type(name).__name__}: {name!r}")
        
        # Case 2: Empty string
        if not name:
            raise ValueError("Pokemon name must be provided")
        
        # Case 3: Name does not exist
        if name not in self._pokemon_index:
            raise InvalidPokemonMoveError(f"Invalid name: '{name}'")
        
        # Case 4: Success
        results = self._pokemon_index[name]

        logger.info("Found pokemon by name", name=name)
        return results

    def get_pokemon_by_move(
        self,
        move: str,
        include_mythical: bool = False,
        include_legendary: bool = False,
        include_ultra_beasts: bool = False
    ) -> dict[str, dict[str, Any]]:
        """
        Get Pokemon that can learn a specific move.

        Args:
            move: Move name (e.g., "thunderbolt")
            include_mythical: Include mythical Pokemon in results
            include_legendary: Include legendary Pokemon in results
            include_ultra_beasts: Include Ultra Beasts in results (postgame only)

        Returns:
            Dict mapping pokemon name to learn methods:
            {
            "pikachu": {"level-up": 36, "machine": True},
            "raichu": {"level-up": 1}
            }

        Raises:
            TypeError: If move is not a string
            ValueError: If move is empty string
            InvalidPokemonMoveError: If move doesn't exist

        Examples:
            >>> get_pokemon_by_move("thunderbolt")
            {'pikachu': {'level-up': 36, 'machine': True}, ...}

            >>> get_pokemon_by_move("thunderbolt", include_legendary=True)
            {'pikachu': {...}, 'zapdos': {...}, ...}
        """
        logger.debug(
            "Searching pokemon by move", 
            move=move,
            include_mythical=include_mythical,
            include_legendary=include_legendary,
            include_ultra_beasts=include_ultra_beasts
            )

        # Validation
        # Case 1: Invalid argument datatype
        if not isinstance(move, str):
            raise TypeError(f"Expected str, got {type(move).__name__}: {move!r}")
        
        # Case 2: Empty string
        if not move:
            raise ValueError("Move name must be provided")
        
        # Case 3: Move does not exist
        if move not in self._move_index:
            raise InvalidPokemonMoveError(f"Invalid move: '{move}'")
        
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
        include_ultra_beasts: bool = False
    ) -> dict[str,dict]:
        """
        Search for Pokemon by base stats, ranked by weighted composite score.

        Args:
            primary_stat: Main stat to optimize (e.g., "attack", "speed")
            secondary_stat: Secondary stat consideration
            min_primary: Minimum value for primary stat (default: 0)
            min_secondary: Minimum value for secondary stat (default: median)
            min_speed: Minimum speed value (default: None, no speed filter)
            include_legendary: Include legendary Pokemon in results
            include_mythical: Include mythical Pokemon in results
            include_ultra_beasts: Include Ultra Beasts in results (postgame only)

        Returns:
            List of Pokemon names, ranked best-first by weighted score.
            Ranking formula: 70% primary + 30% secondary

        Raises:
            TypeError: If stat names are not strings
            ValueError: If stat names are invalid or empty
            NoPokemonFoundError: If no Pokemon match the criteria

        Examples:
            >>> get_pokemon_by_stats("attack", "speed")
            ['garchomp', 'dragapult', 'alakazam', ...]

            >>> get_pokemon_by_stats("attack", "defense", min_primary=120, min_speed=80)
            ['garchomp', 'salamence', ...]  # High attack, good defense, at least 80 speed

            >>> get_pokemon_by_stats("special-attack", "speed", include_legendary=True)
            ['mewtwo', 'alakazam', 'gengar', ...]
        """

        logger.debug(
            "Searching pokemon by stats",
            primary_stat=primary_stat,
            secondary_stat=secondary_stat,
            min_primary=min_primary,
            min_secondary=min_secondary,
            min_speed=min_speed,
            include_legendary=include_legendary,
            include_mythical=include_mythical,
            include_ultra_beasts=include_ultra_beasts
            )
        
        # Case 1: Incorrect argument datatype (Programmer mistake)
        if not isinstance(primary_stat, str):
            raise TypeError(
                f"Expected str for primary_stat, got {type(primary_stat).__name__}"
            )

        if not isinstance(secondary_stat, str):
            raise TypeError(
                f"Expected str for secondary_stat, got {type(secondary_stat).__name__}"
            )

        # Case 2: Empty stat names (Caller mistake)
        if not primary_stat:
            raise ValueError("primary_stat cannot be empty")

        if not secondary_stat:
            raise ValueError("secondary_stat cannot be empty")

        # Case 3: Invalid stat names (Caller mistake)
        valid_stats = {'hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed'}

        if primary_stat not in valid_stats:
            raise ValueError(
                f"Invalid primary_stat: '{primary_stat}'. "
                f"Valid stats: {sorted(valid_stats)}"
            )

        if secondary_stat not in valid_stats:
            raise ValueError(
                f"Invalid secondary_stat: '{secondary_stat}'. "
                f"Valid stats: {sorted(valid_stats)}"
            )

        # Case 4: Default min_secondary to median if not provided
        if min_secondary is None:
            min_secondary = int(self._stat_spreads_index['STAT_MEDIANS'][secondary_stat])

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
            and (min_speed is None or stats['speed'] >= min_speed)
        }

        # Case 7: No Pokemon found matching criteria
        if not candidates:
            raise NoPokemonFoundError(
                f"No Pokemon found with {primary_stat} >= {min_primary} "
                f"and {secondary_stat} >= {min_secondary}"
            )

        # Case 8: Rank by weighted composite score (70% primary, 30% secondary)
        # Higher score = better
        ranked = sorted(
            candidates.items(),
            key=lambda x: (
                STAT_WEIGHT_PRIMARY * x[1][primary_stat] +
                STAT_WEIGHT_SECONDARY * x[1][secondary_stat]
            ),
            reverse=True  # Best first
        )

        logger.info(
            "Found pokemon by stats", 
            primary_stat=primary_stat,
            secondary_sta=secondary_stat,
            min_primary=min_primary,
            min_secondary=min_secondary,
            min_speed=min_speed,
            include_legendary=include_legendary,
            include_mythical=include_mythical,
            include_ultra_beasts=include_ultra_beasts,
            count=len(ranked)
            )
        
        # Return just the names, in ranked order
        return {
            name:stats
            for name,stats in ranked
        }

    def get_pokemon_by_type(
        self,
        *types: str,
        include_legendary: bool = False,
        include_mythical: bool = False,
        include_ultra_beasts: bool = False
    ) -> frozenset[str]:
        """
        Search for Pokemon by type(s).

        Args:
            *types: One or two Pokemon type names (e.g., "fire", "flying")
            include_legendary: Include legendary Pokemon in results
            include_mythical: Include mythical Pokemon in results
            include_ultra_beasts: Include Ultra Beasts in results (postgame only)

        Returns:
            frozenset of Pokemon names matching the type(s)

        Raises:
            TypeError: If arguments are not strings (programmer error)
            ValueError: If no types provided (caller error)
            TooManyTypesError: If more than 2 types provided
            InvalidPokemonTypeError: If any type is not valid
            NoPokemonFoundError: If no Pokemon match the criteria

        Examples:
            >>> get_pokemon_by_type("fire")
            frozenset({'charizard', 'typhlosion', ...})

            >>> get_pokemon_by_type("fire", "flying")
            frozenset({'charizard', 'moltres', ...})

            >>> get_pokemon_by_type("fire", include_legendary=True)
            frozenset({'charizard', 'moltres', 'entei', ...})
        """
        
        logger.debug(
            "Searching pokemon by type", 
            types=types,
            include_legendary=include_legendary,
            include_mythical=include_mythical,
            include_ultra_beasts=include_ultra_beasts
            )
        
        # Case 1: Incorrect arg datatype (Programmer mistake)
        for t in types:
            if not isinstance(t, str):
                raise TypeError(
                    f"Expected str, got {type(t).__name__}: {t!r}"
                )
        
        # Case 2: No pokemon type provided (Caller mistake)
        if not types:
            raise ValueError("At least one Pokemon type must be provided")
        
        # Case 3: Too many args (Caller mistake)
        if len(types) > 2:
            raise TooManyTypesError(
                f"Maximum 2 types allowed, got {len(types)}: {types}"
            )
        
        # Case 4: One or more invalid pokemon types (Caller mistake)
        invalid_types = [t for t in types if t not in self._type_index]
        if invalid_types:
            raise InvalidPokemonTypeError(
                f"Invalid Pokemon type(s): {invalid_types}. "
                f"Valid types: {sorted(self._type_index.keys())}"
            )
        
        # Case 5 & 6: Single or dual type search
        pokemon_list = self._type_index[types[0]] # type: ignore
        for t in types[1:]:
            pokemon_list &= self._type_index[t]
        
        # Case 7: No pokemon found (This might be valid, not always an error)
        if not pokemon_list:
            raise NoPokemonFoundError(
                f"No Pokemon found with type(s): {types}"
            )
        
        # Case 8: Filter by legendary/mythical/ultra beast status
        filtered = frozenset(
            name for name in pokemon_list
            if (include_legendary or not self._pokemon_index[name]["is_legendary"])
            and (include_mythical or not self._pokemon_index[name]["is_mythical"])
            and (include_ultra_beasts or not self._pokemon_index[name]["is_ultra_beast"])
        )
        
        # Case 9: No pokemon after filtering
        if not filtered:
            raise NoPokemonFoundError(
                f"No Pokemon found with type(s) {types} after filtering legendary/mythical"
            )
        
        logger.info(
            "Found pokemon by type", 
            types=types,
            include_legendary=include_legendary,
            include_mythical=include_mythical,
            include_ultra_beasts=include_ultra_beasts,
            count=len(filtered)
            )

        return filtered
    
    def get_type_effectiveness(self, *types: str) -> dict[str, frozenset[str]]:
        """
        Calculate type effectiveness against defending Pokemon.
        
        Args:
            *types: 1-2 defending Pokemon types (e.g., "fire", "flying")
        
        Returns:
            Dict mapping effectiveness to attacking types:
            {"4x": [...], "2x": [...], "neutral": [...], "0.5x": [...], "0x": [...]}
        
        Examples:
            >>> get_type_effectiveness("fire")
            {"2x": ["water", "ground", "rock"], ...}
            
            >>> get_type_effectiveness("fire", "flying")  
            {"4x": ["rock"], "2x": ["water", "electric"], ...}
        """
        
        logger.debug(
            "Searching type matchups", 
            types=types
            )

        # Case 1: Incorrect argument datatype
        for t in types:
            if not isinstance(t, str):
                raise TypeError(f"Expected str, got {type(t).__name__}: {t!r}")
        
        # Case 2: No arguments provided
        if not types:
            raise ValueError("At least one Pokemon type must be provided")
        
        # Case 3: Too many arguments provided
        if len(types) > 2:
            raise TooManyTypesError(
                f"Maximum 2 types allowed, got {len(types)}: {types}"
            )
        
        # Case 4: Invalid pokemon type provided
        invalid_types = [t for t in types if t not in self._type_matchup_index]
        if invalid_types:
            raise InvalidPokemonTypeError(
                f"Invalid type(s): {invalid_types}. "
                f"Valid types: {sorted(self._type_matchup_index.keys())}"
            )
        
        # Case 4 and 5: One or two pokemon provided
        # Calculate effectiveness for each attacking type
        attack_multipliers = {}
        
        for attack_type in self._type_matchup_index.keys():
            multiplier = 1.0
            
            for defending_type in types:
                matchup = self._type_matchup_index[defending_type]
                
                if attack_type in matchup["no_damage_from"]:
                    multiplier = 0.0
                    break
                elif attack_type in matchup["double_damage_from"]:
                    multiplier *= 2
                elif attack_type in matchup["half_damage_from"]:
                    multiplier *= 0.5
            
            attack_multipliers[attack_type] = multiplier
        
        # Group by effectiveness
        by_effectiveness = defaultdict(list)
        for attack_type, mult in attack_multipliers.items():
            if mult == 4.0:
                key = "4x"
            elif mult == 2.0:
                key = "2x"
            elif mult == 1.0:
                key = "1x"
            elif mult == 0.5:
                key = "0.5x"
            elif mult == 0.25:
                key = "0.25x"
            elif mult == 0.0:
                key = "0x"
            else:
                key = f"{mult}x"  # Fallback for weird values
            
            by_effectiveness[key].append(attack_type)

        # Return with frozensets instead of sorted lists
        order = ["4x", "2x", "1x", "0.5x", "0.25x", "0x"]

        ordered = {
            k: frozenset(by_effectiveness[k])
            for k in order
            if k in by_effectiveness
        }

        logger.info(
            "Found type matchups", 
            types=types,
            count = len(ordered)
            )

        return ordered