from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.base import UUIDBase
from uuid import UUID, uuid4

from advanced_alchemy.types import GUID

# Static checker please ignore
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.data.models.pokemon import Pokemon

class Type(UUIDBase):
    __tablename__ = "type"
    id: Mapped[UUID] = mapped_column(GUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(unique=True)
    pokemon: Mapped[list["Pokemon"]] = relationship(secondary="pokemon_type", back_populates="pokemon_types")


# -- Types
# CREATE TABLE types (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL UNIQUE
# );