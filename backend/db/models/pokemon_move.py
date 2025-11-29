from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Table, String, Integer
from litestar.plugins.sqlalchemy import UUIDBase
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

# -- =================
# -- # Junction Table (Many-to-Many)
# -- =================

pokemon_move = Table(
    "pokemon_move",
    UUIDBase.metadata,
    Column("pokemon_id", PG_UUID, ForeignKey("pokemon.id"), primary_key=True),
    Column("move_id", PG_UUID, ForeignKey("move.id"), primary_key=True),
    Column("learn_method", String, nullable=False),
    Column("level", Integer, default=0)   
)

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