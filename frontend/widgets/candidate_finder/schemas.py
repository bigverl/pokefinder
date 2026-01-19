from pydantic import BaseModel as _BaseModel

class BaseModel(_BaseModel):
    # Evidently, this has to be done to enable ORM Mode
    model_config = {"from_attributes": True}

# =============
# DataTable row models for Candidate Finder
# ===========

class MovesTableRow(BaseModel):
    """Row for moves DataTable: [name, level_learned, machine, egg_move]"""
    name: str
    level_learned: str | int
    machine: str
    egg_move: str

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

class VersusTypesTableRow(BaseModel):
    """Row for versus types DataTable: [name, type_combo, 4x, 2x, 1x, 0.5x, 0x]"""
    name: str
    type_combo: str
    four_x: str
    two_x: str
    one_x: str
    half_x: str
    zero_x: str

# =========
# Table models
# ==========

class MovesTable(BaseModel):
    rows: list[MovesTableRow]

class StatsTable(BaseModel):
    rows: list[StatsTableRow]

class TypesTable(BaseModel):
    rows: list[TypesTableRow]

class VersusTypesTable(BaseModel):
    rows: list[VersusTypesTableRow]

# =======
# Full response for frontend
# =========

class CandidateFinderResponse(BaseModel):
    moves_table: MovesTable | None = None
    stats_table: StatsTable | None = None
    types_table: TypesTable | None = None
    versus_types_table: VersusTypesTable | None = None