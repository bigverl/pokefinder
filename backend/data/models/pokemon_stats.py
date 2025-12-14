from __future__ import annotations

from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.base import UUIDBase
from backend.data.models.universal_uuid import UniversalUUID

# Static checker please ignore
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.data.models.pokemon import Pokemon

# -- =================
# -- ## One-to-One Relationship
# -- =================

class PokemonStats(UUIDBase):
    __tablename__ = "pokemon_stats"
    pokemon_id: Mapped[UUID] = mapped_column(UniversalUUID, ForeignKey("pokemon.id"), primary_key=True)
    hp: Mapped[int]
    attack: Mapped[int]
    defense: Mapped[int]
    special_attack: Mapped[int]
    special_defense: Mapped[int]
    speed: Mapped[int]
    pokemon: Mapped["Pokemon"] = relationship(back_populates="stats")

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