-- # Phase 2 Database Schema - Final
-- **Date:** 2025-11-19
-- **Database:** SQLite

-- =================
-- ## Core Tables (Reference Data)
-- =================

-- Pokemon
CREATE TABLE pokemon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    number INTEGER NOT NULL,   -- National Dex #
    height REAL,               -- In meters
    weight REAL,               -- In kilograms
    sprite_url TEXT,           -- PNG sprite URL
    description TEXT,          -- Pokedex description (flavor text)
    genus TEXT,                 -- e.g., "Mouse Pokemon", "Seed Pokemon"
    types TEXT
);
-- Moves
CREATE TABLE moves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    machine_id TEXT  -- NULL if not a TM/HM
);

-- Types
CREATE TABLE types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- =================
-- ## One-to-One Relationships
-- =================

-- Stats (one set per Pokemon)
CREATE TABLE stats (
    pokemon_id INTEGER PRIMARY KEY,
    hp INTEGER NOT NULL,
    attack INTEGER NOT NULL,
    defense INTEGER NOT NULL,
    special_attack INTEGER NOT NULL,
    special_defense INTEGER NOT NULL,
    speed INTEGER NOT NULL,
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id)
);

-- Species flags (one set per Pokemon)
CREATE TABLE species (
    pokemon_id INTEGER PRIMARY KEY,
    is_mythical INTEGER NOT NULL DEFAULT 0,
    is_legendary INTEGER NOT NULL DEFAULT 0,
    is_ultra_beast INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id)
);

-- =================
-- # Junction Tables (Many-to-Many)
-- =================

-- Pokemon Types (Pokemon can have 1-2 types)
CREATE TABLE pokemon_types (
    pokemon_id INTEGER NOT NULL,
    type_id INTEGER NOT NULL,
    slot INTEGER NOT NULL CHECK(slot IN (1, 2)),
    PRIMARY KEY (pokemon_id, type_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY (type_id) REFERENCES types(id)
);

-- Pokemon Moves (Pokemon can learn many moves, moves can be learned by many Pokemon)
CREATE TABLE pokemon_moves (
    pokemon_id INTEGER NOT NULL,
    move_id INTEGER NOT NULL,
    learn_method TEXT NOT NULL,  -- "level-up", "machine", "egg", "tutor"
    level INTEGER NOT NULL DEFAULT 0,  -- Level learned (0 for evolution/machine/egg/tutor moves)
    PRIMARY KEY (pokemon_id, move_id, learn_method, level),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY (move_id) REFERENCES moves(id)
);

-- Type Matchups (Type effectiveness: defender vs attacker)
CREATE TABLE type_matchups (
    defender_type_id INTEGER NOT NULL,
    attacker_type_id INTEGER NOT NULL,
    multiplier REAL NOT NULL CHECK(multiplier IN (0, 0.5, 1, 2, 4)),
    PRIMARY KEY (defender_type_id, attacker_type_id),
    FOREIGN KEY (defender_type_id) REFERENCES types(id),
    FOREIGN KEY (attacker_type_id) REFERENCES types(id)
);

-- =================
-- # Global Metadata
-- =================

-- Stat Quintiles (global stat distribution data)
CREATE TABLE stat_quintiles (
    stat_name TEXT PRIMARY KEY,
    percentile_20 INTEGER NOT NULL,  -- D-tier threshold
    percentile_40 INTEGER NOT NULL,  -- C-tier threshold
    percentile_60 INTEGER NOT NULL,  -- B-tier threshold
    percentile_80 INTEGER NOT NULL,  -- A-tier threshold
    percentile_100 INTEGER NOT NULL, -- S-tier / max
    median INTEGER NOT NULL
);

-- ========
-- Indices
-- ========

CREATE INDEX idx_get_pokemon_by_type ON pokemon_types(type_id);
CREATE INDEX idx_get_pokemon_by_move ON pokemon_moves(move_id);
CREATE INDEX idx_get_type_matchups_by_defender ON type_matchups(defender_type_id);