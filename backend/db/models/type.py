from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from litestar.plugins.sqlalchemy import UUIDBase

# Static checker please ignore
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.db.models.pokemon import Pokemon

class Type(UUIDBase):
    __tablename__ = "type"
    name: Mapped[str] = mapped_column(unique=True)
    pokemon: Mapped[list["Pokemon"]] = relationship(secondary="pokemon_type", back_populates="pokemon_types")


# -- Types
# CREATE TABLE types (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL UNIQUE
# );