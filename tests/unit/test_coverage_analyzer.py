import pytest

from backend.src.lib.repository import JSONRepository
from backend.src.modules.coverage_analyzer.services import CoverageAnalyzerService

# ===========================
# test_my_team_strengths_type_index (repository)
# ============================


# Case 1: Index is populated at startup
@pytest.mark.unit
def test_my_team_strengths_index_populated(fake_repo: JSONRepository):
    index = fake_repo.get_my_team_strengths_type_index()
    assert len(index) > 0


# Case 2: Single-type offensive lookup - fire hits grass/ice/bug/steel for 2x
@pytest.mark.unit
def test_my_team_strengths_fire_offensive(fake_repo: JSONRepository):
    index = fake_repo.get_my_team_strengths_type_index()
    fire_strengths = index["fire"]

    # Fire does 2x to grass, ice, bug, steel (single types)
    assert "grass" in fire_strengths["2x"]
    assert "ice" in fire_strengths["2x"]
    assert "bug" in fire_strengths["2x"]
    assert "steel" in fire_strengths["2x"]

    # Fire does 0.5x to water, rock, fire, dragon
    assert "water" in fire_strengths["0.5x"]
    assert "rock" in fire_strengths["0.5x"]
    assert "fire" in fire_strengths["0.5x"]
    assert "dragon" in fire_strengths["0.5x"]


# Case 3: Single-type offensive lookup - normal does 0x to ghost
@pytest.mark.unit
def test_my_team_strengths_normal_vs_ghost(fake_repo: JSONRepository):
    index = fake_repo.get_my_team_strengths_type_index()
    normal_strengths = index["normal"]

    assert "ghost" in normal_strengths["0x"]


# Case 4: Dual-type offensive lookup - fire/flying hits grass for 4x
@pytest.mark.unit
def test_my_team_strengths_fire_flying_offensive(fake_repo: JSONRepository):
    index = fake_repo.get_my_team_strengths_type_index()

    # Find the fire/flying key (could be either ordering)
    fire_flying_key = None
    for key in index:
        if "/" in key and set(key.split("/")) == {"fire", "flying"}:
            fire_flying_key = key
            break

    assert fire_flying_key is not None, "fire/flying combo not found in index"
    strengths = index[fire_flying_key]

    # Fire/Flying: fire hits grass 2x, flying hits grass 2x -> 4x against single grass
    assert "grass" in strengths["4x"]

    # Fire/Flying: fire hits bug 2x, flying hits bug 2x -> 4x against single bug
    assert "bug" in strengths["4x"]


# Case 5: Index contains both single and dual types
@pytest.mark.unit
def test_my_team_strengths_index_has_single_and_dual(fake_repo: JSONRepository):
    index = fake_repo.get_my_team_strengths_type_index()

    single_types = [k for k in index if "/" not in k]
    dual_types = [k for k in index if "/" in k]

    assert len(single_types) == 18  # all 18 pokemon types
    assert len(dual_types) > 0


# Case 6: Effectiveness categories are frozensets
@pytest.mark.unit
def test_my_team_strengths_values_are_frozensets(fake_repo: JSONRepository):
    index = fake_repo.get_my_team_strengths_type_index()
    fire_strengths = index["fire"]

    for key, value in fire_strengths.items():
        assert isinstance(value, frozenset), f"{key} should be frozenset, got {type(value)}"


# Case 7: Ghost does 0x to normal (the reverse of case 3)
@pytest.mark.unit
def test_my_team_strengths_ghost_vs_normal(fake_repo: JSONRepository):
    index = fake_repo.get_my_team_strengths_type_index()
    ghost_strengths = index["ghost"]

    assert "normal" in ghost_strengths["0x"]


# ===========================
# test_get_teams_type_strengths (service)
# ============================


# Case 1: Single type combo returns strengths
@pytest.mark.unit
def test_get_teams_type_strengths_single_type(coverage_analyzer: CoverageAnalyzerService):
    result = coverage_analyzer.get_teams_type_strengths(["fire"])

    assert "fire" in result
    assert "grass" in result["fire"]["2x"]
    assert "ice" in result["fire"]["2x"]
    assert "bug" in result["fire"]["2x"]
    assert "steel" in result["fire"]["2x"]


# Case 2: Individual types from a dual-type slot
@pytest.mark.unit
def test_get_teams_type_strengths_dual_type_individuals(coverage_analyzer: CoverageAnalyzerService):
    result = coverage_analyzer.get_teams_type_strengths(["fire", "flying"])

    # Should have two entries — one per individual type
    assert len(result) == 2
    assert "fire" in result
    assert "flying" in result

    # fire hits grass for 2x, flying hits grass for 2x
    assert "grass" in result["fire"]["2x"]
    assert "grass" in result["flying"]["2x"]

    # fire hits bug for 2x, flying hits bug for 2x
    assert "bug" in result["fire"]["2x"]
    assert "bug" in result["flying"]["2x"]


# Case 3: Multiple slots
@pytest.mark.unit
def test_get_teams_type_strengths_multiple_slots(coverage_analyzer: CoverageAnalyzerService):
    result = coverage_analyzer.get_teams_type_strengths(["fire", "water", "electric"])

    assert len(result) == 3
    assert "fire" in result
    assert "water" in result
    assert "electric" in result


# Case 4: Unknown type combo is skipped (logged warning, no crash)
@pytest.mark.unit
def test_get_teams_type_strengths_unknown_type(coverage_analyzer: CoverageAnalyzerService):
    result = coverage_analyzer.get_teams_type_strengths(["fire", "faketype"])

    assert len(result) == 1
    assert "fire" in result


# ===========================
# test_get_teams_type_weaknesses (service)
# ============================


# Case 1: Single type combo returns weaknesses
@pytest.mark.unit
def test_get_teams_type_weaknesses_single_type(coverage_analyzer: CoverageAnalyzerService):
    result = coverage_analyzer.get_teams_type_weaknesses(["fire"])

    assert "fire" in result
    # Fire is weak to water, ground, rock
    assert "water" in result["fire"]["2x"]
    assert "ground" in result["fire"]["2x"]
    assert "rock" in result["fire"]["2x"]


# Case 2: Dual type combo - fire/flying is 4x weak to rock
@pytest.mark.unit
def test_get_teams_type_weaknesses_dual_type(coverage_analyzer: CoverageAnalyzerService):
    result = coverage_analyzer.get_teams_type_weaknesses(["fire-flying"])

    assert len(result) == 1
    key = list(result.keys())[0]
    assert set(key.split("/")) == {"fire", "flying"}

    # fire/flying is 4x weak to rock
    assert "rock" in result[key]["4x"]
    # fire/flying is 2x weak to water and electric
    assert "water" in result[key]["2x"]
    assert "electric" in result[key]["2x"]


# Case 3: Multiple slots
@pytest.mark.unit
def test_get_teams_type_weaknesses_multiple_slots(coverage_analyzer: CoverageAnalyzerService):
    result = coverage_analyzer.get_teams_type_weaknesses(["fire", "grass"])

    assert len(result) == 2
    assert "fire" in result
    assert "grass" in result

    # Fire weak to water, grass weak to fire - different weaknesses
    assert "water" in result["fire"]["2x"]
    assert "fire" in result["grass"]["2x"]


# ===========================
# test_normalize_type_combo (service)
# ============================


# Case 1: Single type passes through
@pytest.mark.unit
def test_normalize_type_combo_single(coverage_analyzer: CoverageAnalyzerService):
    assert coverage_analyzer._normalize_type_combo("fire") == "fire"


# Case 2: Hyphen converted to slash
@pytest.mark.unit
def test_normalize_type_combo_dual(coverage_analyzer: CoverageAnalyzerService):
    result = coverage_analyzer._normalize_type_combo("fire-flying")
    assert "/" in result
    assert set(result.split("/")) == {"fire", "flying"}


# Case 3: Canonical ordering is respected
@pytest.mark.unit
def test_normalize_type_combo_canonical_order(coverage_analyzer: CoverageAnalyzerService):
    forward = coverage_analyzer._normalize_type_combo("fire-flying")
    reverse = coverage_analyzer._normalize_type_combo("flying-fire")
    # Both should resolve to the same canonical key
    assert forward == reverse


# ===========================
# test_build_response (service)
# ============================


# Case 1: Response has both tables
@pytest.mark.unit
def test_build_response_both_tables(coverage_analyzer: CoverageAnalyzerService):
    response = coverage_analyzer.build_response(["fire", "water"])

    assert response.team_strengths_table is not None
    assert response.team_weaknesses_table is not None


# Case 2: Tables have rows populated
@pytest.mark.unit
def test_build_response_row_count(coverage_analyzer: CoverageAnalyzerService):
    response = coverage_analyzer.build_response(["fire", "water", "grass"])

    assert response.team_strengths_table is not None
    assert response.team_weaknesses_table is not None
    assert len(response.team_strengths_table.rows) > 0
    assert len(response.team_weaknesses_table.rows) > 0


# Case 3: Rows have correct schema fields and fire hits grass at 2x
@pytest.mark.unit
def test_build_response_rows_populated(coverage_analyzer: CoverageAnalyzerService):
    response = coverage_analyzer.build_response(["fire"])

    assert response.team_strengths_table is not None
    rows = response.team_strengths_table.rows
    assert len(rows) > 0
    grass_rows = [r for r in rows if r.enemy_type == "grass" and r.friendly_type == "fire"]
    assert len(grass_rows) == 1
    assert grass_rows[0].effectiveness == "2x"


# Case 4: Dual type produces rows for both individual types (strengths)
@pytest.mark.unit
def test_build_response_dual_type_slot(coverage_analyzer: CoverageAnalyzerService):
    response = coverage_analyzer.build_response(["fire-flying"])

    assert response.team_strengths_table is not None
    rows = response.team_strengths_table.rows
    friendly_types = {r.friendly_type for r in rows}
    assert "fire" in friendly_types
    assert "flying" in friendly_types
    # grass should be hit at 4x (fire 2x * flying neutral? no — strengths are per individual type)
    # fire hits grass at 2x, flying hits grass at 2x — both should appear
    grass_rows = [r for r in rows if r.enemy_type == "grass"]
    assert len(grass_rows) >= 1


# Case 5: Full team of 6 slots produces rows for both tables
@pytest.mark.unit
def test_build_response_full_team(coverage_analyzer: CoverageAnalyzerService):
    response = coverage_analyzer.build_response(["fire", "water", "grass", "electric", "psychic", "dark"])

    assert response.team_strengths_table is not None
    assert response.team_weaknesses_table is not None
    assert len(response.team_strengths_table.rows) > 0
    assert len(response.team_weaknesses_table.rows) > 0
