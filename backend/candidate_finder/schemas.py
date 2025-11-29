from pydantic import BaseModel as _BaseModel, RootModel
from typing import Any

class BaseModel(_BaseModel):
    # Evidently, this has to be done to enable ORM Mode
    model_config = {"from_attributes": True}

class PokemonInfoResponse(BaseModel):
    name: str
    number: int
    types: list[str]
    height: float
    weight: float
    sprite_url: str
    description: str
    genus: str

class PokemonTypeResponse(BaseModel):
    type_combo: str
    pokemon_list: frozenset[str]

class PokemonMoveResponse(BaseModel):
    move_name: str
    pokemon_list: dict[str,Any]

class PokemonStatsResponse(RootModel):
    root: dict[str,dict]

class TypeMatchupResponse(RootModel):
    root: dict[str, frozenset[str]]