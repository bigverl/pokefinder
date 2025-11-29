from __future__ import annotations

import uuid
from uuid import UUID
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from litestar import Litestar, get
from litestar.plugins.sqlalchemy import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyPlugin, UUIDBase
from typing import Optional

class Base(DeclarativeBase):
    pass

# -- Pokemon
# CREATE TABLE pokemon (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL UNIQUE,
#     number INTEGER NOT NULL,   -- National Dex #
#     height REAL,               -- In meters
#     weight REAL,               -- In kilograms
#     sprite_url TEXT,           -- PNG sprite URL
#     description TEXT,          -- Pokedex description (flavor text)
#     genus TEXT,                 -- e.g., "Mouse Pokemon", "Seed Pokemon"
#     types TEXT
# );
class Pokemon(UUIDBase):
    __tablename__ = "pokemon"
    name: Mapped[str] = mapped_column(unique=True)
    number: Mapped[int] = mapped_column(unique=True)
    height: Mapped[float]
    weight: Mapped[float]
    sprite_url: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    genus: Mapped[str]
    types_display: Mapped[str]
    stats: Mapped[Stats] = relationship(back_populates="pokemon")
    species: Mapped[Species] = relationship(back_populates="pokemon")
    pokemon_types: Mapped[list[PokemonTypes]] = relationship(back_populates="pokemon")
    pokemon_moves: Mapped[list[PokemonMoves]] = relationship(back_populates="pokemon")

# -- Moves
# CREATE TABLE moves (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL UNIQUE,
#     machine_id TEXT  -- NULL if not a TM/HM
# );
class Moves(UUIDBase):
    __tablename__ = "moves"
    name: Mapped[str] = mapped_column(unique=True)
    number: Mapped[int] = mapped_column(unique=True)
    machine_id: Mapped[Optional[str]] = mapped_column(unique=True)

# -- Types
# CREATE TABLE types (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL UNIQUE
# );
class Types(UUIDBase):
    __tablename__ = "types"
    name: Mapped[str] = mapped_column(unique=True)

# -- =================
# -- ## One-to-One Relationships
# -- =================

# -- Stats (one set per Pokemon)
# CREATE TABLE stats (
#     pokemon_id INTEGER PRIMARY KEY,
#     hp INTEGER NOT NULL,
#     attack INTEGER NOT NULL,
#     defense INTEGER NOT NULL,
#     special_attack INTEGER NOT NULL,
#     special_defense INTEGER NOT NULL,
#     speed INTEGER NOT NULL,
#     FOREIGN KEY (pokemon_id) REFERENCES pokemon(id)
# );
class Stats(UUIDBase):
    __tablename__ = "stats"
    pokemon_id: Mapped[UUID] = mapped_column(ForeignKey("pokemon.id"), primary_key=True)
    hp: Mapped[int]
    attack: Mapped[int]
    defense: Mapped[int]
    special_attack: Mapped[int]
    special_defense: Mapped[int]
    speed: Mapped[int]
    pokemon: Mapped[Pokemon] = relationship(back_populates="pokemon")

# -- Species flags (one set per Pokemon)
# CREATE TABLE species (
#     pokemon_id INTEGER PRIMARY KEY,
#     is_mythical INTEGER NOT NULL DEFAULT 0,
#     is_legendary INTEGER NOT NULL DEFAULT 0,
#     is_ultra_beast INTEGER NOT NULL DEFAULT 0,
#     FOREIGN KEY (pokemon_id) REFERENCES pokemon(id)
# );

class Species(Base):
    __tablename__ = "species"
    pokemon_id: Mapped[UUID] = mapped_column(ForeignKey("pokemon.id"), primary_key=True)
    is_legendary: Mapped[bool] = mapped_column(default=0)
    is_mythical: Mapped[bool] = mapped_column(default=0)
    is_ultra_beast: Mapped[bool] = mapped_column(default=0)
    pokemon: Mapped[Pokemon] = relationship(back_populates="species")
# -- =================
# -- # Junction Tables (Many-to-Many)
# -- =================

# -- Pokemon Types (Pokemon can have 1-2 types)
# CREATE TABLE pokemon_types (
#     pokemon_id INTEGER NOT NULL,
#     type_id INTEGER NOT NULL,
#     slot INTEGER NOT NULL CHECK(slot IN (1, 2)),
#     PRIMARY KEY (pokemon_id, type_id),
#     FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
#     FOREIGN KEY (type_id) REFERENCES types(id)
# );

class PokemonTypes(Base):
    __tablename__ = "pokemon_types"
    pokemon_id: Mapped[UUID] = mapped_column(ForeignKey("pokemon.id"), primary_key=True)
    type_id: Mapped[UUID] = mapped_column(ForeignKey("types.id"), primary_key=True)
    slot: Mapped[int]
    types: Mapped[Types] = relationship()
    pokemon: Mapped[Pokemon] = relationship(back_populates="pokemon_types")
    __table_args__ = (CheckConstraint("slot IN (1, 2)", name="check_slot_valid"))

# -- Pokemon Moves (Pokemon can learn many moves, moves can be learned by many Pokemon)
# CREATE TABLE pokemon_moves (
#     pokemon_id INTEGER NOT NULL,
#     move_id INTEGER NOT NULL,
#     learn_method TEXT NOT NULL,  -- "level-up", "machine", "egg", "tutor"
#     level INTEGER NOT NULL DEFAULT 0,  -- Level learned (0 for evolution/machine/egg/tutor moves)
#     PRIMARY KEY (pokemon_id, move_id, learn_method, level),
#     FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
#     FOREIGN KEY (move_id) REFERENCES moves(id)
# );
class PokemonMoves(Base):
    __tablename__ = "pokemon_moves"
    pokemon_id: Mapped[UUID] = mapped_column(ForeignKey("pokemon.id"), primary_key=True)
    move_id: Mapped[UUID] = mapped_column(ForeignKey("moves.id"), primary_key=True)
    learn_method: Mapped[str]
    level: Mapped[int] = mapped_column(default=0)
    moves: Mapped[Moves] = relationship()
    pokemon: Mapped[Pokemon] = relationship(back_populates="pokemon_moves")

# -- Type Matchups (Type effectiveness: defender vs attacker)
# CREATE TABLE type_matchups (
#     defender_type_id INTEGER NOT NULL,
#     attacker_type_id INTEGER NOT NULL,
#     multiplier REAL NOT NULL CHECK(multiplier IN (0, 0.5, 1, 2, 4)),
#     PRIMARY KEY (defender_type_id, attacker_type_id),
#     FOREIGN KEY (defender_type_id) REFERENCES types(id),
#     FOREIGN KEY (attacker_type_id) REFERENCES types(id)
# );
class Matchups(Base):
    __tablename__ = "matchups"
    defender_type_id: Mapped[UUID] = mapped_column(ForeignKey("types.id"), primary_key=True)
    attacker_type_id: Mapped[UUID] = mapped_column(ForeignKey("types.id"), primary_key=True)
    multiplier: Mapped[float]
    defender_type: Mapped[Types] = relationship(foreign_keys=[defender_type_id])
    attacker_type: Mapped[Types] = relationship(foreign_keys=[attacker_type_id])
    __table_args__ = (CheckConstraint("multiplier IN (0, 0.5, 1, 2, 4)", name="check_multiplier_valid"))
# -- =================
# -- # Global Metadata
# -- =================

# -- Stat Quintiles (global stat distribution data)
# CREATE TABLE stat_quintiles (
#     stat_name TEXT PRIMARY KEY,
#     percentile_20 INTEGER NOT NULL,  -- D-tier threshold
#     percentile_40 INTEGER NOT NULL,  -- C-tier threshold
#     percentile_60 INTEGER NOT NULL,  -- B-tier threshold
#     percentile_80 INTEGER NOT NULL,  -- A-tier threshold
#     percentile_100 INTEGER NOT NULL, -- S-tier / max
#     median INTEGER NOT NULL
# );
class Quintiles(Base):
    __tablename__ = "quintiles"
    stat_name: Mapped[str] = mapped_column(primary_key=True)
    percentile_20: Mapped[int]
    percentile_40: Mapped[int]
    percentile_60: Mapped[int]
    percentile_80: Mapped[int]
    percentile_100: Mapped[int]
    median: Mapped[int]