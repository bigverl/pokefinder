from __future__ import annotations

from sqlalchemy import ForeignKey, CheckConstraint, Table, Column, Float, Index
from advanced_alchemy.base import UUIDBase
from backend.data.models.universal_uuid import UniversalUUID

# -- =================
# -- # Junction Table (Many-to-Many)
# -- =================

type_matchup = Table(
    "type_matchup",
    UUIDBase.metadata,
    Column("defender_type_id", UniversalUUID, ForeignKey("type.id"), primary_key=True),
    Column("attacker_type_id", UniversalUUID, ForeignKey("type.id"), primary_key=True),
    Column("multiplier", Float),
    CheckConstraint("multiplier IN (0, 0.5, 1, 2, 4)", name="check_multiplier_valid"),
    Index("idx_get_type_matchups_by_defender", "defender_type_id")
)

# -- Type Matchups (Type effectiveness: defender vs attacker)
# CREATE TABLE type_matchups (
#     defender_type_id INTEGER NOT NULL,
#     attacker_type_id INTEGER NOT NULL,
#     multiplier REAL NOT NULL CHECK(multiplier IN (0, 0.5, 1, 2, 4)),
#     PRIMARY KEY (defender_type_id, attacker_type_id),
#     FOREIGN KEY (defender_type_id) REFERENCES types(id),
#     FOREIGN KEY (attacker_type_id) REFERENCES types(id)
# );