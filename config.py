from pathlib import Path
import os

BASE_DIR = Path(__file__).parent
DATA_CACHE_DIR = BASE_DIR / "data_cache"

# Dataset selection (use env var to switch between unbound and pokerogue)
DATASET = os.getenv("DATASET", "pokerogue")  # Options: "unbound" or "pokerogue"
DATASET_DIR = DATA_CACHE_DIR / DATASET

# Database paths (Phase 2+)
DATABASES_DIR = BASE_DIR / "databases"
DB_NAME = os.getenv("DB_NAME", f"pokemon_{DATASET}_sqlite.db")  # pokemon_unbound_sqlite.db or pokemon_pokerogue_sqlite.db
SQLITE_DB_PATH = DATABASES_DIR / DB_NAME

# JSON cache paths (Phase 1 - dataset-specific)
MACHINE_MOVES_PATH = DATASET_DIR / "machine_moves.json"
POKEMON_BY_MOVE_PATH = DATASET_DIR / "pokemon_by_move.json"
POKEMON_BY_TYPE_PATH = DATASET_DIR / "pokemon_by_type.json"
POKEMON_INFO_PATH = DATASET_DIR / "pokemon_info.json"
POKEMON_MOVELIST_PATH = DATASET_DIR / "pokemon_movelist.json"
POKEMON_SPECIES_PATH = DATASET_DIR / "pokemon_species.json"
POKEMON_STATS_PATH = DATASET_DIR / "pokemon_stats.json"
STAT_SPREADS_PATH = DATASET_DIR / "stat_spreads.json"
TYPE_MATCHUPS_PATH = DATASET_DIR / "type_matchups.json"

# CORS
ALLOWED_CORS_ORIGINS: list[str] = ["*"]

# Rate limiter
