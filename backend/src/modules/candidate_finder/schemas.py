from pydantic import BaseModel as _BaseModel

class BaseModel(_BaseModel):
    # Evidently, this has to be done to enable ORM Mode
    model_config = {"from_attributes": True}

# =============
# DataTable row models for Candidate Finder
# ===========

class MovesTableRow(BaseModel):
    """Row for moves DataTable: [name, level_learned, machine, egg_move]"""
    pokemon_name: str
    move_name: str
    level_learned: str | int | None
    machine: str | None
    egg_move: str | None

class StatsTableRow(BaseModel):
    """Row for stats DataTable: [name, attack, defense, special_attack, special_defense, speed]"""
    name: str
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

class TypesTableRow(BaseModel):
    """Row for types DataTable: [name, type1, type2]"""
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