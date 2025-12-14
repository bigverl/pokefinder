from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Table, String, Integer, Index
from advanced_alchemy.base import UUIDBase
from advanced_alchemy.types import GUID

# -- =================
# -- # Junction Table (Many-to-Many)
# -- =================

pokemon_move = Table(
    "pokemon_move",
    UUIDBase.metadata,
    Column("pokemon_id", GUID, ForeignKey("pokemon.id"), primary_key=True),
    Column("move_name", String, primary_key=True),  # String, no FK
    Column("learn_method", String, nullable=False, primary_key=True),
    Column("level", Integer, default=0, primary_key=True),
    Index("idx_pokemon_moves_by_pokemon", "pokemon_id"),
    Index("idx_pokemon_moves_by_move", "move_name")
)