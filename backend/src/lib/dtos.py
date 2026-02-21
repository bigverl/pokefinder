from pydantic import BaseModel


class PokemonMove(BaseModel):
    pokemon_name: str
    move_name: str
    learn_method: str
    level: int


class PokemonStats(BaseModel):
    pokemon_name: str
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


class PokemonType(BaseModel):
    pokemon_name: str
    type_name: str
    slot: int


class Pokemon(BaseModel):
    name: str
    display_name: str
    number: int
    height: float
    weight: float
    sprite_url: str
    description: str
    genus: str
    type_display: str
    is_legendary: bool
    is_mythical: bool
    is_ultra_beast: bool


class StatSpread(BaseModel):
    stat_name: str
    percentile_20: int
    percentile_40: int
    percentile_60: int
    percentile_80: int
    percentile_100: int
    median: int


class Tm(BaseModel):
    name: str
    machine_id: str | None


class TypeMatchup(BaseModel):
    defender_type: str
    attacker_type: str
    multiplier: float
