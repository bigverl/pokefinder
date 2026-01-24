from pydantic import BaseModel as _BaseModel

class BaseModel(_BaseModel):
    # Evidently, this has to be done to enable ORM Mode
    model_config = {"from_attributes": True}

# =============
# DataTable row models for Candidate Finder
# ===========

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

class VersusTypesTable(BaseModel):
    rows: list[VersusTypesTableRow]

# =======
# Full response for frontend
# =========

class CoverageAnalyzerResponse(BaseModel):
    versus_types_table: VersusTypesTable | None = None