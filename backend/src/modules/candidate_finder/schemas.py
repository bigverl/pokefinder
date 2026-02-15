from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):
    # evidently, this has to be done to enable ORM Mode
    model_config = {"from_attributes": True}


# =============
# DataTable row models for Candidate Finder
# ===========


class MovesTableRow(BaseModel):
    pokemon_name: str
    move_name: str
    level_learned: str | int | None
    machine: str | None
    egg_move: str | None


class StatsTableRow(BaseModel):
    name: str
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


class TypesTableRow(BaseModel):
    name: str
    type1: str
    type2: str | None


# =========
# Table models
# ==========


class MovesTable(BaseModel):
    rows: list[MovesTableRow]


class StatsTable(BaseModel):
    rows: list[StatsTableRow]


class TypesTable(BaseModel):
    rows: list[TypesTableRow]


# =======
# Full response for frontend
# =========


class CandidateFinderResponse(BaseModel):
    moves_table: MovesTable | None = None
    stats_table: StatsTable | None = None
    types_table: TypesTable | None = None
