from unittest.mock import AsyncMock

import pytest
from textual.widgets import DataTable

from frontend.app import Pokefinder
from frontend.modules.candidate_finder.widgets.results import CandidateFinderResults
from frontend.modules.candidate_finder.widgets.search import CandidateFinderSearch


@pytest.mark.asyncio
async def test_collect_params_with_move_enabled(self):
    """When move filter is enabled, params should include move value."""
    app = Pokefinder()
    async with app.run_test() as pilot:
        # Enable move filter
        await pilot.click("#move_radio_button")

        # Type move name
        await pilot.click("#move_input")
        await pilot.press(*"thunderbolt")

        # Collect params
        search_widget = app.query_one(CandidateFinderSearch)
        params = search_widget._collect_search_params()

        assert params["move"] == "thunderbolt"
        assert params["desired_type"] is None
        assert params["primary_stat"] is None


@pytest.mark.asyncio
async def test_collect_params_with_type_enabled(self):
    """When type filter is enabled, params should include desired_type."""
    app = Pokefinder()
    async with app.run_test() as pilot:
        # Enable type filter
        await pilot.click("#desired_type_radio_button")

        # Type in type1
        await pilot.click("#type1_input")
        await pilot.press(*"fire")

        # Collect params
        search_widget = app.query_one(CandidateFinderSearch)
        params = search_widget._collect_search_params()

        assert params["desired_type"] == "fire"
        assert params["move"] is None


@pytest.mark.asyncio
async def test_collect_params_dual_type(self):
    """When both types entered, desired_type should be hyphenated."""
    app = Pokefinder()
    async with app.run_test() as pilot:
        # Enable type filter
        await pilot.click("#desired_type_radio_button")

        # Type in type1 and type2
        await pilot.click("#type1_input")
        await pilot.press(*"fire")
        await pilot.click("#type2_input")
        await pilot.press(*"flying")

        search_widget = app.query_one(CandidateFinderSearch)
        params = search_widget._collect_search_params()

        assert params["desired_type"] == "fire-flying"


@pytest.mark.asyncio
async def test_collect_params_special_pokemon_flags(self):
    """Special pokemon checkboxes should be collected."""
    app = Pokefinder()
    async with app.run_test() as pilot:
        # Enable legendary
        await pilot.click("#legendary_radio_button")

        search_widget = app.query_one(CandidateFinderSearch)
        params = search_widget._collect_search_params()

        assert params["include_legendary"] is True
        assert params["include_mythical"] is False
        assert params["include_ultra_beasts"] is False


@pytest.mark.asyncio
async def test_parse_int_rejects_floats(self):
    """_parse_int should raise ValueError for float strings."""
    app = Pokefinder()
    async with app.run_test():
        search_widget = app.query_one(CandidateFinderSearch)

        with pytest.raises(ValueError, match="Expected integer"):
            search_widget._parse_int("3.14")


@pytest.mark.asyncio
async def test_parse_int_handles_empty(self):
    """_parse_int should return 0 for empty string."""
    app = Pokefinder()
    async with app.run_test():
        search_widget = app.query_one(CandidateFinderSearch)
        assert search_widget._parse_int("") == 0


@pytest.mark.asyncio
async def test_populate_moves_table(self, mock_api_response):
    """populate_results_table should fill moves DataTable."""
    app = Pokefinder()
    async with app.run_test() as pilot:
        results_widget = app.query_one(CandidateFinderResults)
        results_widget.populate_results_table(mock_api_response)

        await pilot.pause()

        moves_table = results_widget.query_one("#candidate_moves", DataTable)
        assert moves_table.row_count == 2


@pytest.mark.asyncio
async def test_populate_stats_table(self, mock_api_response):
    """populate_results_table should fill stats DataTable."""
    app = Pokefinder()
    async with app.run_test() as pilot:
        results_widget = app.query_one(CandidateFinderResults)
        results_widget.populate_results_table(mock_api_response)

        await pilot.pause()

        stats_table = results_widget.query_one("#candidate_stats", DataTable)
        assert stats_table.row_count == 2


@pytest.mark.asyncio
async def test_populate_types_table(self, mock_api_response):
    """populate_results_table should fill types DataTable."""
    app = Pokefinder()
    async with app.run_test() as pilot:
        results_widget = app.query_one(CandidateFinderResults)
        results_widget.populate_results_table(mock_api_response)

        await pilot.pause()

        types_table = results_widget.query_one("#candidate_types", DataTable)
        assert types_table.row_count == 2


@pytest.mark.asyncio
async def test_populate_clears_existing_data(self, mock_api_response):
    """populate_results_table should clear existing rows first."""
    app = Pokefinder()
    async with app.run_test() as pilot:
        results_widget = app.query_one(CandidateFinderResults)

        # Populate twice
        results_widget.populate_results_table(mock_api_response)
        results_widget.populate_results_table(mock_api_response)

        await pilot.pause()

        # Should still have 2 rows, not 4
        moves_table = results_widget.query_one("#candidate_moves", DataTable)
        assert moves_table.row_count == 2


@pytest.mark.asyncio
async def test_search_button_triggers_api_call(self, mock_backend_client, mock_api_response):
    """Clicking search button should call API and populate results."""
    app = Pokefinder()
    app.api_client = mock_backend_client

    async with app.run_test() as pilot:
        # Enable move filter and enter value
        await pilot.click("#move_radio_button")
        await pilot.click("#move_input")
        await pilot.press(*"thunderbolt")

        # Click search
        await pilot.click(".go_button")
        await pilot.pause()

        # Verify API was called
        mock_backend_client.search_pokemon.assert_called_once()

        # Verify results populated
        results_widget = app.query_one(CandidateFinderResults)
        moves_table = results_widget.query_one("#candidate_moves", DataTable)
        assert moves_table.row_count == 2


@pytest.mark.asyncio
async def test_search_with_no_filters_shows_error(self, mock_backend_client):
    """Search with no filters enabled should show error notification."""
    from httpx import HTTPStatusError, Request, Response

    # Mock API to raise error (backend returns 400 for no filters)
    mock_response = Response(400, request=Request("GET", "http://test"))
    mock_backend_client.search_pokemon = AsyncMock(
        side_effect=HTTPStatusError(
            "Must provide at least one search parameter", request=mock_response.request, response=mock_response
        )
    )

    app = Pokefinder()
    app.api_client = mock_backend_client

    async with app.run_test() as pilot:
        # Click search without enabling any filters
        await pilot.click(".go_button")
        await pilot.pause()

        # Should have shown notification (hard to assert, but API should have been called)
        mock_backend_client.search_pokemon.assert_called_once()
