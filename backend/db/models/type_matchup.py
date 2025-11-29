from __future__ import annotations


from uuid import UUID
from sqlalchemy import ForeignKey, CheckConstraint, Table, Column, Float
from litestar.plugins.sqlalchemy import UUIDBase
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

# -- =================
# -- # Junction Table (Many-to-Many)
# -- =================

type_matchup = Table(
    "type_matchup",
    UUIDBase.metadata,
    Column("defender_type_id", PG_UUID, ForeignKey("type.id"), primary_key=True),
    Column("attacker_type_id", PG_UUID, ForeignKey("type.id"), primary_key=True),
    Column("multiplier", Float),
    CheckConstraint("multiplier IN (0, 0.5, 1, 2, 4)", name="check_multiplier_valid")
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