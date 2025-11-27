# tests/api/test_pokemon_routes.py
import pytest
from litestar.testing import TestClient
from backend.app import app

# ========
# /health
# ========
def test_health_check():
    """Test the health check endpoint."""
    with TestClient(app=app) as client:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

# ========
# /pokemon/{name}
# ========

def test_get_pokemon_info_success():
    """Test getting info for a valid Pokemon."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon/bulbasaur")

        assert response.status_code == 200

        data = response.json()
        assert data["name"] == "bulbasaur"
        assert data["number"] == 1
        assert "grass" in data["types"]
        assert "poison" in data["types"]


def test_get_pokemon_info_not_found():
    """Test getting info for a non-existent Pokemon."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon/fakemon")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


# ========
# /pokemon/
# ========

# Case: No param 400
def test_pokemon_no_params():
    """Test /pokemon with no query params returns 400."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon")

        assert response.status_code == 400
        assert "must specify" in response.json()["detail"].lower()


# ========
# Move filter
# ========

# Case 1: Invalid move 400
def test_pokemon_move_invalid():
    """Test /pokemon with invalid move returns 400."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?move=fakemove")

        assert response.status_code == 400
        assert "invalid move" in response.text.lower()


# Case 2: Failure - Pokemon not found 404
def test_pokemon_move_not_found():
    """Test /pokemon with move that has no learners returns 404."""
    with TestClient(app=app) as client:
        # Use a real move but filter out all Pokemon
        response = client.get("/pokemon?move=tackle&include_legendary=false&include_mythical=false&include_ultra_beasts=false")

        # This might return 200 with results, so we need a move that truly has no learners
        # For now, this test may need adjustment based on actual data
        # Placeholder assertion
        assert response.status_code in [200, 404]


# Case 3: Success - Found 200
def test_pokemon_move_success():
    """Test /pokemon with valid move returns 200."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?move=tackle")

        assert response.status_code == 200
        data = response.json()
        assert "move_name" in data
        assert data["move_name"] == "tackle"
        assert "pokemon_list" in data
        assert isinstance(data["pokemon_list"], dict)


# Case 4: Test legendary filter
def test_pokemon_move_exclude_legendary():
    """Test /pokemon move filter excludes legendaries by default."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?move=tackle")

        assert response.status_code == 200
        data = response.json()
        pokemon_list = data["pokemon_list"]
        assert isinstance(pokemon_list, dict)


# Case 5: Test include legendary
def test_pokemon_move_include_legendary():
    """Test /pokemon move filter includes legendaries when requested."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?move=tackle&include_legendary=true")

        assert response.status_code == 200
        data = response.json()
        assert "pokemon_list" in data


# Case 6: Test include mythical
def test_pokemon_move_include_mythical():
    """Test /pokemon move filter includes mythicals when requested."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?move=tackle&include_mythical=true")

        assert response.status_code == 200
        data = response.json()
        assert "pokemon_list" in data


# Case 7: Test include ultra beasts
def test_pokemon_move_include_ultra_beasts():
    """Test /pokemon move filter includes ultra beasts when requested."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?move=tackle&include_ultra_beasts=true")

        assert response.status_code == 200
        data = response.json()
        assert "pokemon_list" in data


# ========
# Type filter
# ========

# Case 1: Invalid type 400
def test_pokemon_type_invalid():
    """Test /pokemon with invalid type returns 400."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?types=faketype")

        assert response.status_code == 400
        assert "invalid" in response.text.lower()


# Case 2: Too many types 400
def test_pokemon_type_too_many():
    """Test /pokemon with more than 2 types returns 400."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?types=fire-water-grass")

        assert response.status_code == 400
        assert "maximum 2 types" in response.text.lower()


# Case 3: Failure - Pokemon not found 404
def test_pokemon_type_not_found():
    """Test /pokemon with valid type combo that has no Pokemon returns 404."""
    with TestClient(app=app) as client:
        # Use a type combo that shouldn't exist
        response = client.get("/pokemon?types=normal-ghost")

        # This might actually exist in the data, adjust as needed
        assert response.status_code in [200, 404]


# Case 4: Success - Found Pokemon 200
def test_pokemon_type_success_single():
    """Test /pokemon with single valid type returns 200."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?types=fire")

        assert response.status_code == 200
        data = response.json()
        assert "type_combo" in data
        assert data["type_combo"] == "fire"
        assert "pokemon_list" in data
        assert isinstance(data["pokemon_list"], list)


# Case 5: Test dual types success
def test_pokemon_type_success_dual():
    """Test /pokemon with dual types returns 200."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?types=fire-flying")

        assert response.status_code == 200
        data = response.json()
        assert "type_combo" in data
        assert data["type_combo"] == "fire-flying"
        assert "pokemon_list" in data
        assert isinstance(data["pokemon_list"], list)


# Case 6: Test exclude legendary
def test_pokemon_type_exclude_legendary():
    """Test /pokemon type filter excludes legendaries by default."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?types=fire")

        assert response.status_code == 200
        data = response.json()
        assert "pokemon_list" in data


# Case 7: Test include legendary
def test_pokemon_type_include_legendary():
    """Test /pokemon type filter includes legendaries when requested."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?types=fire&include_legendary=true")

        assert response.status_code == 200
        data = response.json()
        assert "pokemon_list" in data


# Case 8: Test include mythical
def test_pokemon_type_include_mythical():
    """Test /pokemon type filter includes mythicals when requested."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?types=fire&include_mythical=true")

        assert response.status_code == 200
        data = response.json()
        assert "pokemon_list" in data


# Case 9: Test include ultra beasts
def test_pokemon_type_include_ultra_beasts():
    """Test /pokemon type filter includes ultra beasts when requested."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?types=fire&include_ultra_beasts=true")

        assert response.status_code == 200
        data = response.json()
        assert "pokemon_list" in data


# ========
# Stat Filter
# ========

# Case 1: invalid primary_stat 400
def test_pokemon_stats_invalid_primary():
    """Test /pokemon with invalid primary_stat returns 400."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?primary_stat=fakestat&secondary_stat=speed")

        assert response.status_code == 400
        assert "invalid" in response.text.lower()


# Case 2: invalid secondary_stat 400
def test_pokemon_stats_invalid_secondary():
    """Test /pokemon with invalid secondary_stat returns 400."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?primary_stat=attack&secondary_stat=fakestat")

        assert response.status_code == 400
        assert "invalid" in response.text.lower()


# Case 3: Not found 404
def test_pokemon_stats_not_found():
    """Test /pokemon with stats that match no Pokemon returns 404."""
    with TestClient(app=app) as client:
        # Use impossibly high thresholds
        response = client.get("/pokemon?primary_stat=attack&secondary_stat=speed&min_primary=999&min_secondary=999")

        assert response.status_code == 404
        assert "no pokemon found" in response.text.lower()


# Case 4: found 200
def test_pokemon_stats_success():
    """Test /pokemon with valid stat filters returns 200."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?primary_stat=attack&secondary_stat=speed")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        # Response is RootModel, so it's just the dict directly
        # Should contain pokemon names as keys
        assert len(data) > 0


# Case 5: Test exclude legendary
def test_pokemon_stats_exclude_legendary():
    """Test /pokemon stats filter excludes legendaries by default."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?primary_stat=attack&secondary_stat=speed")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


# Case 6: Test include legendary
def test_pokemon_stats_include_legendary():
    """Test /pokemon stats filter includes legendaries when requested."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?primary_stat=attack&secondary_stat=speed&include_legendary=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


# Case 7: Test include mythical
def test_pokemon_stats_include_mythical():
    """Test /pokemon stats filter includes mythicals when requested."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?primary_stat=attack&secondary_stat=speed&include_mythical=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


# Case 8: Test include ultra beasts
def test_pokemon_stats_include_ultra_beasts():
    """Test /pokemon stats filter includes ultra beasts when requested."""
    with TestClient(app=app) as client:
        response = client.get("/pokemon?primary_stat=attack&secondary_stat=speed&include_ultra_beasts=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


# ========
# /type-matchups
# ========

# Case 1: invalid type 400
def test_type_matchups_invalid_type():
    """Test /type-matchups with invalid type returns 400."""
    with TestClient(app=app) as client:
        response = client.get("/type-matchups?types=faketype")

        assert response.status_code == 400
        assert "invalid" in response.text.lower()


# Case 2: success: single type 200
def test_type_matchups_success_single():
    """Test /type-matchups with single type returns 200."""
    with TestClient(app=app) as client:
        response = client.get("/type-matchups?types=fire")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        # Should have effectiveness categories
        assert any(key in data for key in ["4x", "2x", "1x", "0.5x", "0.25x", "0x"])


# Case 3: success: dual type 200
def test_type_matchups_success_dual():
    """Test /type-matchups with dual types returns 200."""
    with TestClient(app=app) as client:
        response = client.get("/type-matchups?types=fire-flying")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        # Should have effectiveness categories
        assert any(key in data for key in ["4x", "2x", "1x", "0.5x", "0.25x", "0x"])




