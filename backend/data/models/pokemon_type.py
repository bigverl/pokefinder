from __future__ import annotations

from sqlalchemy import ForeignKey, CheckConstraint, Table, Column, Integer, Index
from advanced_alchemy.base import UUIDBase
from backend.data.models.universal_uuid import UniversalUUID

# -- =================
# -- # Junction Table (Many-to-Many)
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

pokemon_type = Table(
    "pokemon_type",
    UUIDBase.metadata,
    Column("pokemon_id", UniversalUUID, ForeignKey("pokemon.id"), primary_key=True),
    Column("type_id", UniversalUUID, ForeignKey("type.id"), primary_key=True),
    Column("slot", Integer),
    CheckConstraint("slot IN (1, 2)", name="check_slot_valid"),
    Index("idx_get_pokemon_by_type", "type_id")
    )