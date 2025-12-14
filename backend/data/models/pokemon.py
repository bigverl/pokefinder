from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from litestar.plugins.sqlalchemy import UUIDBase
from backend.data.models.pokemon_type import pokemon_type


# Static checker please ignore
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.data.models.pokemon_stats import PokemonStats
    from backend.data.models.type import Type

class Pokemon(UUIDBase):
    __tablename__ = "pokemon"
    name: Mapped[str] = mapped_column(unique=True)
    display_name: Mapped[str] = mapped_column(unique=True)
    number: Mapped[int]
    height: Mapped[float]
    weight: Mapped[float]
    sprite_url: Mapped[str]
    description: Mapped[str]
    genus: Mapped[str]
    type_display: Mapped[str]
    stats: Mapped["PokemonStats"] = relationship(back_populates="pokemon")
    is_legendary: Mapped[bool] = mapped_column(default=0)
    is_mythical: Mapped[bool] = mapped_column(default=0)
    is_ultra_beast: Mapped[bool] = mapped_column(default=0)
    pokemon_types: Mapped[list["Type"]] = relationship(secondary=pokemon_type, back_populates="pokemon")
    
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