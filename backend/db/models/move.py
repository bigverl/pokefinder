from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from litestar.plugins.sqlalchemy import UUIDBase
from typing import Optional

# Static checker please ignore
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.db.models.pokemon import Pokemon

class Move(UUIDBase):
    __tablename__ = "move"
    name: Mapped[str] = mapped_column(unique=True)
    number: Mapped[int] = mapped_column(unique=True)
    machine_id: Mapped[Optional[str]] = mapped_column(unique=True)
    pokemon: Mapped[list["Pokemon"]] = relationship(secondary="pokemon_move", back_populates="pokemon_moves")

# -- Moves
# CREATE TABLE moves (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL UNIQUE,
#     machine_id TEXT  -- NULL if not a TM/HM
# );