# tests/component/test_api.py
# Component tests: HTTP -> controller -> service -> repo
import pytest
import structlog

logger = structlog.get_logger(__name__)


# ========
# /health
# ========
@pytest.mark.component
def test_health_check(test_client):
    """Test the health check endpoint."""
    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


# ========
# /search_pokemon/ (search endpoint)
# ========


# Case: No param - returns 400 error
@pytest.mark.component
def test_pokemon_no_params(test_client):
    """Test /search_pokemon with no query params returns 400 error."""
    response = test_client.get("/search_pokemon")

    assert response.status_code == 400


# ========
# Move filter
# ========


# Case 1: Invalid move 400
@pytest.mark.component
def test_pokemon_move_invalid(test_client):
    """Test /search_pokemon with invalid move returns 400."""
    response = test_client.get("/search_pokemon?move=fakemove")

    assert response.status_code == 400
    assert "invalid move" in response.text.lower()


# Case 2: Success - Found 200
@pytest.mark.component
def test_pokemon_move_success(test_client):
    """Test /search_pokemon with valid move returns 200 with moves_table and types_table."""
    response = test_client.get("/search_pokemon?move=tackle")

    assert response.status_code == 200
    data = response.json()

    # Should have moves_table populated
    moves_table = data.get("moves_table")
    assert moves_table is not None
    assert "rows" in moves_table
    assert len(moves_table["rows"]) > 0

    # Check row structure
    first_row = moves_table["rows"][0]
    assert "move_name" in first_row
    assert "level_learned" in first_row
    assert "machine" in first_row
    assert "egg_move" in first_row

    # Should always have types_table populated
    types_table = data.get("types_table")
    assert types_table is not None
    assert len(types_table["rows"]) > 0


# Case 3: Test legendary filter
@pytest.mark.component
def test_pokemon_move_exclude_legendary(test_client):
    """Test /search_pokemon move filter excludes legendaries by default."""
    response = test_client.get("/search_pokemon?move=psychic")

    assert response.status_code == 200
    data = response.json()

    # Check that legendary Pokemon are not in results
    types_table = data.get("types_table")
    pokemon_names = [row["name"] for row in types_table["rows"]]
    assert "mewtwo" not in pokemon_names
    assert "latias" not in pokemon_names


# Case 4: Test include legendary
@pytest.mark.component
def test_pokemon_move_include_legendary(test_client):
    """Test /search_pokemon move filter includes legendaries when requested."""
    response = test_client.get("/search_pokemon?move=psychic&include_legendary=true")

    assert response.status_code == 200
    data = response.json()

    # Should have results
    assert data.get("moves_table") is not None
    moves_table = data.get("moves_table")
    assert len(moves_table["rows"]) > 0


# Case 5: Test include mythical
@pytest.mark.component
def test_pokemon_move_include_mythical(test_client):
    """Test /search_pokemon move filter includes mythicals when requested."""
    response = test_client.get("/search_pokemon?move=psychic&include_mythical=true")

    assert response.status_code == 200
    data = response.json()
    assert data.get("moves_table") is not None


# Case 6: Test include ultra beasts
@pytest.mark.component
def test_pokemon_move_include_ultra_beasts(test_client):
    """Test /search_pokemon move filter includes ultra beasts when requested."""
    response = test_client.get("/search_pokemon?move=psychic&include_ultra_beasts=true")

    assert response.status_code == 200
    data = response.json()
    assert data.get("moves_table") is not None


# ========
# Type filter (desired_type parameter)
# ========


# Case 1: Invalid type 400
@pytest.mark.component
def test_pokemon_type_invalid(test_client):
    """Test /search_pokemon with invalid desired_type returns 400."""
    response = test_client.get("/search_pokemon?desired_type=faketype")

    assert response.status_code == 400
    assert "invalid" in response.text.lower()


# Case 2: Too many types 400
@pytest.mark.component
def test_pokemon_type_too_many(test_client):
    """Test /search_pokemon with more than 2 types returns 400."""
    response = test_client.get("/search_pokemon?desired_type=fire-water-grass")

    assert response.status_code == 400
    assert "maximum 2 types" in response.text.lower()


# Case 3: Success - Single type 200
@pytest.mark.component
def test_pokemon_type_success_single(test_client):
    """Test /search_pokemon with single valid desired_type returns 200 with types_table."""
    response = test_client.get("/search_pokemon?desired_type=fire")
    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    data = response.json()

    assert response.status_code == 200

    # Should have types_table populated
    assert data.get("types_table") is not None
    types_table = data.get("types_table")
    assert len(types_table["rows"]) > 0

    # Check that all returned Pokemon have fire type
    for row in types_table["rows"]:
        assert "fire" in [row["type1"], row["type2"]]


# Case 4: Success - Dual types 200
@pytest.mark.component
def test_pokemon_type_success_dual(test_client):
    """Test /search_pokemon with dual desired_type returns 200."""
    response = test_client.get("/search_pokemon?desired_type=fire-flying")

    assert response.status_code == 200
    data = response.json()

    # Should have types_table populated
    assert data.get("types_table") is not None
    types_table = data.get("types_table")
    assert len(types_table["rows"]) > 0

    # Check that all returned Pokemon have BOTH fire and flying
    for row in types_table["rows"]:
        types = [row["type1"], row["type2"]]
        assert "fire" in types
        assert "flying" in types


# Case 5: Test exclude legendary
@pytest.mark.component
def test_pokemon_type_exclude_legendary(test_client):
    """Test /search_pokemon desired_type filter excludes legendaries by default."""
    response = test_client.get("/search_pokemon?desired_type=psychic")

    assert response.status_code == 200
    data = response.json()

    # Check that legendary Pokemon are not in results
    types_table = data.get("types_table")
    pokemon_names = [row["name"] for row in types_table["rows"]]
    assert "mewtwo" not in pokemon_names
    assert "latias" not in pokemon_names


# Case 6: Test include legendary
@pytest.mark.component
def test_pokemon_type_include_legendary(test_client):
    """Test /search_pokemon desired_type filter includes legendaries when requested."""
    response = test_client.get("/search_pokemon?desired_type=psychic&include_legendary=true")

    assert response.status_code == 200
    data = response.json()
    assert data.get("types_table") is not None


# Case 7: Test include mythical
@pytest.mark.component
def test_pokemon_type_include_mythical(test_client):
    """Test /search_pokemon desired_type filter includes mythicals when requested."""
    response = test_client.get("/search_pokemon?desired_type=psychic&include_mythical=true")

    assert response.status_code == 200
    data = response.json()
    assert data.get("types_table") is not None


# Case 8: Test include ultra beasts
@pytest.mark.component
def test_pokemon_type_include_ultra_beasts(test_client):
    """Test /search_pokemon desired_type filter includes ultra beasts when requested."""
    response = test_client.get("/search_pokemon?desired_type=psychic&include_ultra_beasts=true")

    assert response.status_code == 200
    data = response.json()
    assert data.get("types_table") is not None


# ========
# Stat Filter
# ========


# Case 1: invalid primary_stat 400
@pytest.mark.component
def test_pokemon_stats_invalid_primary(test_client):
    """Test /search_pokemon with invalid primary_stat returns 400."""
    response = test_client.get("/search_pokemon?primary_stat=fakestat&secondary_stat=speed")

    assert response.status_code == 400
    assert "invalid" in response.text.lower()


# Case 2: invalid secondary_stat 400
@pytest.mark.component
def test_pokemon_stats_invalid_secondary(test_client):
    """Test /search_pokemon with invalid secondary_stat returns 400."""
    response = test_client.get("/search_pokemon?primary_stat=attack&secondary_stat=fakestat")

    assert response.status_code == 400
    assert "invalid" in response.text.lower()


# Case 3: Not found 404
@pytest.mark.component
def test_pokemon_stats_not_found(test_client):
    """Test /search_pokemon with stats that match no Pokemon returns 404."""
    # Use impossibly high thresholds
    response = test_client.get(
        "/search_pokemon?primary_stat=attack&secondary_stat=speed&min_primary=999&min_secondary=999"
    )

    assert response.status_code == 404
    assert "no pokemon found" in response.text.lower()


# Case 4: Success 200
@pytest.mark.component
def test_pokemon_stats_success(test_client):
    """Test /search_pokemon with valid stat filters returns 200 with stats_table and types_table."""
    response = test_client.get("/search_pokemon?primary_stat=attack&secondary_stat=speed")

    assert response.status_code == 200
    data = response.json()

    # Should have stats_table populated
    assert data.get("stats_table") is not None
    stats_table = data.get("stats_table")
    assert len(stats_table["rows"]) > 0

    # Check row structure
    first_row = stats_table["rows"][0]
    assert "name" in first_row
    assert "attack" in first_row
    assert "defense" in first_row
    assert "special_attack" in first_row
    assert "special_defense" in first_row
    assert "speed" in first_row

    # Should always have types_table populated
    assert data.get("types_table") is not None
    types_table = data.get("types_table")
    assert len(types_table["rows"]) > 0


# Case 5: Test exclude legendary
@pytest.mark.component
def test_pokemon_stats_exclude_legendary(test_client):
    """Test /search_pokemon stats filter excludes legendaries by default."""
    response = test_client.get("/search_pokemon?primary_stat=attack&secondary_stat=speed")

    assert response.status_code == 200
    data = response.json()

    # Check that legendary Pokemon are not in results
    stats_table = data.get("stats_table")
    pokemon_names = [row["name"] for row in stats_table["rows"]]
    assert "mewtwo" not in pokemon_names
    assert "rayquaza" not in pokemon_names


# Case 6: Test include legendary
@pytest.mark.component
def test_pokemon_stats_include_legendary(test_client):
    """Test /search_pokemon stats filter includes legendaries when requested."""
    response = test_client.get("/search_pokemon?primary_stat=attack&secondary_stat=speed&include_legendary=true")

    assert response.status_code == 200
    data = response.json()
    assert data.get("stats_table") is not None


# Case 7: Test include mythical
@pytest.mark.component
def test_pokemon_stats_include_mythical(test_client):
    """Test /search_pokemon stats filter includes mythicals when requested."""
    response = test_client.get("/search_pokemon?primary_stat=attack&secondary_stat=speed&include_mythical=true")

    assert response.status_code == 200
    data = response.json()
    assert data.get("stats_table") is not None


# Case 8: Test include ultra beasts
@pytest.mark.component
def test_pokemon_stats_include_ultra_beasts(test_client):
    """Test /search_pokemon stats filter includes ultra beasts when requested."""
    response = test_client.get("/search_pokemon?primary_stat=attack&secondary_stat=speed&include_ultra_beasts=true")

    assert response.status_code == 200
    data = response.json()
    assert data.get("stats_table") is not None


# ========
# /team_coverage (coverage analyzer endpoint)
# ========


# Case 1: No slots - returns 400
@pytest.mark.component
def test_team_coverage_no_slots(test_client):
    """Test /team_coverage with no slots returns 400."""
    response = test_client.get("/team_coverage")

    assert response.status_code == 400


# Case 2: Single slot success - returns 200 with both tables
@pytest.mark.component
def test_team_coverage_single_slot(test_client):
    """Test /team_coverage with single slot returns 200."""
    response = test_client.get("/team_coverage?slot_1=fire")

    assert response.status_code == 200
    data = response.json()

    assert data.get("team_strengths_table") is not None
    assert data.get("team_weaknesses_table") is not None

    strengths = data["team_strengths_table"]
    assert len(strengths["rows"]) > 0

    weaknesses = data["team_weaknesses_table"]
    assert len(weaknesses["rows"]) > 0


# Case 3: Dual type slot - returns 200 with correct effectiveness
@pytest.mark.component
def test_team_coverage_dual_type_slot(test_client):
    """Test /team_coverage with dual type slot returns correct 4x data."""
    response = test_client.get("/team_coverage?slot_1=fire-flying")

    assert response.status_code == 200
    data = response.json()

    # Strengths: fire hits grass 2x, flying hits grass 2x — both should appear
    strengths_rows = data["team_strengths_table"]["rows"]
    grass_rows = [r for r in strengths_rows if r["enemy_type"] == "grass"]
    assert len(grass_rows) >= 1

    # Weaknesses: fire/flying is 4x weak to rock
    weaknesses_rows = data["team_weaknesses_table"]["rows"]
    rock_4x = [r for r in weaknesses_rows if r["enemy_type"] == "rock" and r["effectiveness"] == "4x"]
    assert len(rock_4x) == 1


# Case 4: Multiple slots - returns rows for all slots
@pytest.mark.component
def test_team_coverage_multiple_slots(test_client):
    """Test /team_coverage with multiple slots returns rows for each type."""
    response = test_client.get("/team_coverage?slot_1=fire&slot_2=water&slot_3=grass")

    assert response.status_code == 200
    data = response.json()

    # Should have rows covering all 3 types
    strengths_types = {r["friendly_type"] for r in data["team_strengths_table"]["rows"]}
    assert "fire" in strengths_types
    assert "water" in strengths_types
    assert "grass" in strengths_types

    weaknesses_types = {r["friendly_type"] for r in data["team_weaknesses_table"]["rows"]}
    assert len(weaknesses_types) == 3


# Case 5: Full team of 6 slots
@pytest.mark.component
def test_team_coverage_full_team(test_client):
    """Test /team_coverage with all 6 slots returns 200."""
    response = test_client.get(
        "/team_coverage?slot_1=fire&slot_2=water&slot_3=grass&slot_4=electric&slot_5=psychic&slot_6=dark"
    )

    assert response.status_code == 200
    data = response.json()

    # Should have rows for all 6 types in both tables
    strengths_types = {r["friendly_type"] for r in data["team_strengths_table"]["rows"]}
    assert len(strengths_types) == 6

    weaknesses_types = {r["friendly_type"] for r in data["team_weaknesses_table"]["rows"]}
    assert len(weaknesses_types) == 6


# Case 6: Row structure has expected fields
@pytest.mark.component
def test_team_coverage_row_structure(test_client):
    """Test /team_coverage rows have correct field structure."""
    response = test_client.get("/team_coverage?slot_1=fire")

    assert response.status_code == 200
    data = response.json()

    row = data["team_strengths_table"]["rows"][0]
    assert "effectiveness" in row
    assert "enemy_type" in row
    assert "friendly_type" in row
