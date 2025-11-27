
import json
import aiosqlite
import structlog

from pathlib import Path
from typing import Any

logger = structlog.get_logger(__name__)

# Json Index Paths
from config import (
    MACHINE_MOVES_PATH,
    POKEMON_BY_MOVE_PATH,
    POKEMON_BY_TYPE_PATH,
    POKEMON_SPECIES_PATH,
    POKEMON_STATS_PATH,
    STAT_SPREADS_PATH,
    TYPE_MATCHUPS_PATH,
    SQLITE_DB_PATH
)

# Base Abstract Class
class PokemonRepository:
    """Abstract base class for Pokemon data repositories."""

    def __init__(self):
        pass

    def get_move_index(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Returns move index: {move_name: {pokemon_name: {learn_method: data}}}"""
        return {}

    def get_species_index(self) -> dict[str, dict[str, bool]]:
        """Returns species flags: {pokemon_name: {is_legendary: bool, is_mythical: bool, is_ultra_beast: bool}}"""
        return {}

    def get_stat_index(self) -> dict[str, dict[str, int]]:
        """Returns base stats: {pokemon_name: {stat_name: value}}"""
        return {}

    def get_stat_spread_index(self) -> dict[str, Any]:
        """Returns stat quintiles: {category: {stat_name: value}}"""
        return {}

    def get_type_index(self) -> dict[str, frozenset[str]]:
        """Returns type index: {type_name: frozenset(pokemon_names)}"""
        return {}

    def get_type_matchup_index(self) -> dict[str, dict[str, frozenset[str]]]:
        """Returns matchups: {defending_type: {category: frozenset(attacking_types)}}"""
        return {}

    def get_machine_moves_index(self) -> dict:
        """Returns machine moves: {move_name: machine_id}"""
        return {}

# Phase 1
class JsonRepository(PokemonRepository):
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def get_move_index(self) -> dict[str, dict[str, dict[str, Any]]]:
        """
        Structure:
        {
        "thunderbolt": {
            "pikachu": {"level-up": 36, "machine": True},
            "raichu": {"level-up": 1, "machine": True}
        }
        }
        """
        cache_path = POKEMON_BY_MOVE_PATH
        try:
            with open(cache_path, "r") as f:            
                return json.load(f)
        except FileNotFoundError as e:
            logger.error("Index file not found", filepath=str(cache_path), error=str(e))
            raise
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON", filepath=str(cache_path), error=str(e))
            raise


    def get_species_index(self) -> dict[str, dict[str, bool]]:
        """
        Structure:
        {
            "pikachu": {"is_legendary": False, "is_mythical": False, "is_ultra_beast": False},
            ...
        }
        """
        cache_path = POKEMON_SPECIES_PATH
        try:
            with open(cache_path, "r") as f:            
                return json.load(f)
        except FileNotFoundError as e:
            logger.error("Index file not found", filepath=str(cache_path), error=str(e))
            raise
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON", filepath=str(cache_path), error=str(e))
            raise

    def get_stat_index(self) -> dict[str, dict[str, int]]:
        """
        Structure:
        {
            "pikachu": {"hp": 35, "attack": 55, "defense": 40, "special-attack": 50, ...},
            ...
        }
        """
        cache_path = POKEMON_STATS_PATH
        try:
            with open(cache_path, "r") as f:            
                return json.load(f)
        except FileNotFoundError as e:
            logger.error("Index file not found", filepath=str(cache_path), error=str(e))
            raise
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON", filepath=str(cache_path), error=str(e))
            raise

    def get_stat_spread_index(self) -> dict[str, dict[str, int]]:
        """
        Structure:
        {
            "STAT_MEDIANS": {"hp": 65, "attack": 75, ...},
            "QUINTILES": {...},
            ...
        }
        """
        cache_path = STAT_SPREADS_PATH
        try:
            with open(cache_path, "r") as f:            
                return json.load(f)
        except FileNotFoundError as e:
            logger.error("Index file not found", filepath=str(cache_path), error=str(e))
            raise
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON", filepath=str(cache_path), error=str(e))
            raise

    def get_type_index(self) -> dict[str, frozenset[str]]:
        """
        Structure:
        {
            "fire": frozenset({"charizard", "arcanine", ...}),
            ...
        }
        """
        cache_path = POKEMON_BY_TYPE_PATH
        try:
            with open(cache_path, "r") as f:            
                data = json.load(f)
                return {type_name: frozenset(pokemon_list) for type_name, pokemon_list in data.items()}       
        except FileNotFoundError as e:
            logger.error("Index file not found", filepath=str(cache_path), error=str(e))
            raise
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON", filepath=str(cache_path), error=str(e))
            raise

    def get_type_matchup_index(self) -> dict[str, dict[str, frozenset[str]]]:
        """
        Structure:
        {
            "fire": {
                "double_damage_from": frozenset({"water", "ground", "rock"}),
                "half_damage_from": frozenset({"fire", "grass", ...}),
                "no_damage_from": frozenset()
            },
            ...
        }
        """
        cache_path = TYPE_MATCHUPS_PATH
        try:
            with open(cache_path, "r") as f:            
                data = json.load(f)
                return {
                    defending_type: {
                        category: frozenset(types)
                        for category, types in matchups.items()
                    }
                    for defending_type, matchups in data.items()
                }    
        except FileNotFoundError as e:
            logger.error("Index file not found", filepath=str(cache_path), error=str(e))
            raise
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON", filepath=str(cache_path), error=str(e))
            raise
        
    def get_machine_moves_index(self)  -> dict:
        """
        Structure:
        {
        
        }
        """
        cache_path = MACHINE_MOVES_PATH
        try:
            with open(cache_path, "r") as f:            
                return json.load(f)
        except FileNotFoundError as e:
            logger.error("Index file not found", filepath=str(cache_path), error=str(e))
            raise
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON", filepath=str(cache_path), error=str(e))
            raise

# Phase 2
class SQLiteRepository(PokemonRepository):
    def __init__(self, db_path: Path | None = None):
        """Initialize repository and load all indexes from database.

        Args:
            db_path: Optional path to database file. Defaults to SQLITE_DB_PATH from config.
        """
        self.db_path = db_path if db_path is not None else SQLITE_DB_PATH

    @classmethod
    async def create(cls, db_path: Path | None = None):
        self = cls(db_path)
        await self._load_all_indexes()
        return self

    async def _load_all_indexes(self):
        """Load all 6 indexes from database on initialization."""
        try:
            async with aiosqlite.connect(self.db_path) as con:
                con.row_factory = aiosqlite.Row
                try:
                    # Run all 6 queries and cache results
                    self._move_index = await self._query_move_index(con)
                    self._species_index = await self._query_species_index(con)
                    self._stat_index = await self._query_stat_index(con)
                    self._stat_spread_index = await self._query_stat_spread_index(con)
                    self._type_index = await self._query_type_index(con)
                    self._type_matchup_index = await self._query_type_matchup_index(con)
                    self._machine_moves_index = await self._query_machine_moves_index(con)
                except aiosqlite.DatabaseError as e:
                    logger.error("Database query failed", error=str(e))
                    raise
        except aiosqlite.OperationalError as e:
            logger.error("Database failed to open", file_path=str(self.db_path), error=str(e))
            raise

        logger.info(
            "All indexes loaded successfully",
            db_path=str(self.db_path),
            pokemon_count=len(self._species_index),
            move_count=len(self._move_index)
            )

    async def _query_move_index(self, con) -> dict[str, dict[str, dict[str, Any]]]:
        """Query move index: {move_name: {pokemon_name: {learn_method: level/True}}}"""
        async with con.execute("""
            SELECT m.name as move_name, p.name as pokemon_name, pm.learn_method, pm.level
            FROM pokemon_moves pm
            JOIN pokemon p ON pm.pokemon_id = p.id
            JOIN moves m ON pm.move_id = m.id
            ORDER BY m.name, p.name
        """) as cur:
            rows = await cur.fetchall()

        move_index = {}
        for row in rows:
            move_name = row["move_name"]
            pokemon_name = row["pokemon_name"]
            method = row["learn_method"]
            level = row["level"]

            # Initialize move entry
            if move_name not in move_index:
                move_index[move_name] = {}

            # Initialize pokemon entry for this move
            if pokemon_name not in move_index[move_name]:
                move_index[move_name][pokemon_name] = {}

            # Add learn method
            if method == "level-up":
                move_index[move_name][pokemon_name][method] = level
            else:
                # machine, tutor, egg stored as boolean
                move_index[move_name][pokemon_name][method] = True

        logger.info(
            "Move index created successfully",
            move_count=len(move_index)
            )
        return move_index

    async def _query_species_index(self, con) -> dict[str, dict[str, bool]]:
        """Query species flags: {pokemon_name: {is_legendary: bool, ...}}"""
        async with con.execute("""
            SELECT p.name, s.is_legendary, s.is_mythical, s.is_ultra_beast
            FROM species s
            JOIN pokemon p ON s.pokemon_id = p.id
        """) as cur:
            rows = await cur.fetchall()

        species_index = {}
        for row in rows:
            species_index[row["name"]] = {
                "is_legendary": bool(row["is_legendary"]),
                "is_mythical": bool(row["is_mythical"]),
                "is_ultra_beast": bool(row["is_ultra_beast"])
            }

        logger.info(
            "Species index created successfully",
            species_count=len(species_index)
            )
        return species_index

    async def _query_stat_index(self, con) -> dict[str, dict[str, int]]:
        """Query base stats: {pokemon_name: {stat_name: value}}"""
        async with con.execute("""
            SELECT p.name, s.hp, s.attack, s.defense,
                   s.special_attack, s.special_defense, s.speed
            FROM stats s
            JOIN pokemon p ON s.pokemon_id = p.id
        """) as cur:
            rows = await cur.fetchall()

        stat_index = {}
        for row in rows:
            stat_index[row["name"]] = {
                "hp": row["hp"],
                "attack": row["attack"],
                "defense": row["defense"],
                "special_attack": row["special_attack"],
                "special_defense": row["special_defense"],
                "speed": row["speed"]
            }

        logger.info(
            "Stat index created successfully",
            stat_count=len(stat_index))
        return stat_index

    async def _query_stat_spread_index(self, con) -> dict[str, Any]:
        """Query stat distribution: {STAT_MEDIANS: {...}, QUINTILES: {...}}"""
        async with con.execute("""
            SELECT stat_name, percentile_20, percentile_40, percentile_60,
                   percentile_80, percentile_100, median
            FROM stat_quintiles
        """) as cur:
            rows = await cur.fetchall()
        
        medians = {}
        quintiles = {}
        for row in rows:
            stat_name = row["stat_name"]

            # Store median
            medians[stat_name] = row["median"]

            # Store quintiles
            quintiles[stat_name] = {
                "20th": row["percentile_20"],
                "40th": row["percentile_40"],
                "60th": row["percentile_60"],
                "80th": row["percentile_80"],
                "100th": row["percentile_100"]
            }
        
        logger.info(
            "Stat spread index created successfully") # No need for count here.
        return {
            "STAT_MEDIANS": medians,
            "QUINTILES": quintiles
        }

    async def _query_type_index(self, con) -> dict[str, frozenset[str]]:
        """Query type index: {type_name: frozenset(pokemon_names)}"""
        async with con.execute("""
            SELECT t.name as type_name, p.name as pokemon_name
            FROM pokemon_types pt
            JOIN types t ON pt.type_id = t.id
            JOIN pokemon p ON pt.pokemon_id = p.id
            ORDER BY t.name
        """) as cur:
            rows = await cur.fetchall()

        type_index = {}
        for row in rows:
            type_name = row["type_name"]
            pokemon_name = row["pokemon_name"]

            if type_name not in type_index:
                type_index[type_name] = []

            type_index[type_name].append(pokemon_name)

        
        # Convert lists to frozensets
        filtered = {type_name: frozenset(pokemon_list)
                for type_name, pokemon_list in type_index.items()}
        
        logger.info(
            "Type index created successfully",
            type_count=len(filtered)
            )
        return filtered

    async def _query_type_matchup_index(self, con) -> dict[str, dict[str, frozenset[str]]]:
        """Query type matchups: {defending_type: {category: frozenset(attacking_types)}}"""
        async with con.execute("""
            SELECT defender.name as defender_type,
                   attacker.name as attacker_type,
                   tm.multiplier
            FROM type_matchups tm
            JOIN types defender ON tm.defender_type_id = defender.id
            JOIN types attacker ON tm.attacker_type_id = attacker.id
        """) as cur:
            rows = await cur.fetchall()

        matchup_index = {}
        for row in rows:
            defender = row["defender_type"]
            attacker = row["attacker_type"]
            multiplier = row["multiplier"]

            # Initialize defender entry
            if defender not in matchup_index:
                matchup_index[defender] = {
                    "double_damage_from": [],
                    "half_damage_from": [],
                    "no_damage_from": []
                }

            # Categorize by multiplier
            if multiplier == 0.0:
                matchup_index[defender]["no_damage_from"].append(attacker)
            elif multiplier == 0.5:
                matchup_index[defender]["half_damage_from"].append(attacker)
            elif multiplier == 2.0 or multiplier == 4.0:
                matchup_index[defender]["double_damage_from"].append(attacker)

        # Convert lists to frozensets
        matchups = {
            defender: {
                category: frozenset(attackers)
                for category, attackers in categories.items()
            }
            for defender, categories in matchup_index.items()
        }


        logger.info(
            "Type matchup index created successfully",
            matchup_count=len(matchups))
        return matchups

    async def _query_machine_moves_index(self, con) -> dict:
        """Query machine moves index: {move_name: machine_id}"""
        async with con.execute("""
            SELECT name, machine_id FROM moves WHERE machine_id IS NOT NULL;
        """) as cur:
            rows = await cur.fetchall()
        
        machine_moves_index = {}
        for row in rows:
           machine_moves_index[row["name"]] = row["machine_id"]

        logger.info(
            "Machine moves index created successfully",
            machine_moves_count=len(machine_moves_index))
        return machine_moves_index
    
        
    # Public interface - return cached indexes
    def get_move_index(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Returns move index: {move_name: {pokemon_name: {learn_method: data}}}"""
        return self._move_index

    def get_species_index(self) -> dict[str, dict[str, bool]]:
        """Returns species flags: {pokemon_name: {is_legendary: bool, ...}}"""
        return self._species_index

    def get_stat_index(self) -> dict[str, dict[str, int]]:
        """Returns base stats: {pokemon_name: {stat_name: value}}"""
        return self._stat_index

    def get_stat_spread_index(self) -> dict[str, Any]:
        """Returns stat quintiles: {category: {stat_name: value}}"""
        return self._stat_spread_index

    def get_type_index(self) -> dict[str, frozenset[str]]:
        """Returns type index: {type_name: frozenset(pokemon_names)}"""
        return self._type_index

    def get_type_matchup_index(self) -> dict[str, dict[str, frozenset[str]]]:
        """Returns matchups: {defending_type: {category: frozenset(attacking_types)}}"""
        return self._type_matchup_index

    def get_machine_moves_index(self) -> dict:
        return self._machine_moves_index

# Phase 5(?)
class PostgreSQLRepository(PokemonRepository):
    def __init__(self):
        pass

    def get_move_index(self) -> dict[str, dict[str, dict[str, Any]]]:
        return {}

    def get_species_index(self) -> dict[str, dict[str, bool]]:
        return {}

    def get_stat_index(self) -> dict[str, dict[str, int]]:
        return {}

    def get_stat_spread_index(self) -> dict[str, Any]:
        return {}

    def get_type_index(self) -> dict[str, frozenset[str]]:
        return {}

    def get_type_matchup_index(self) -> dict[str, dict[str, frozenset[str]]]:
        return {}

