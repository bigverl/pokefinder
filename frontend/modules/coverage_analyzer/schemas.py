from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):
    model_config = {"from_attributes": True}


# =============
# DataTable row models for Coverage Analyzer
# ===========


class TypeCoverageTableRow(BaseModel):
    effectiveness: str
    enemy_type: str
    friendly_type: str


# =========
# Table models
# ==========


class TypeCoverageTable(BaseModel):
    rows: list[TypeCoverageTableRow]


# =======
# Full response for frontend
# =========


class CoverageAnalyzerResponse(BaseModel):
    team_strengths_table: TypeCoverageTable | None = None
    team_weaknesses_table: TypeCoverageTable | None = None
