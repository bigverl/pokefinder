from typing import TYPE_CHECKING
from textual import on
from textual.app import ComposeResult

from textual.containers import Vertical


from textual.widgets import (
    DataTable,
    TabPane,
    TabbedContent
    )

from backend.src.modules.candidate_finder.schemas import CandidateFinderResponse

if TYPE_CHECKING:
    from frontend.app import Pokefinder

"""
Data Table Columns
"""

moves_columns = ["pokemon", "move", "level learned", "machine", "egg move"]

stats_columns = ["name", "attack", "defense", "special attack", "special defense", "speed"]

types_columns = ["name", "type 1", "type 2"]

type_matchups_columns = ["type combo", "4x", "2x", "1x", "0.5x", "0x"]

class CandidateFinderResults(Vertical):
    """
    Left Tab Pane representing candidate finder feature
    """

    # Populate table
    def populate_results_table(self, data: CandidateFinderResponse):
        # Moves table
        results_moves_table = self.query_one("#candidate_moves", DataTable)
        results_moves_table.clear()
        if data.moves_table:
            for row in data.moves_table.rows:
                results_moves_table.add_row(
                    row.pokemon_name,
                    row.move_name,
                    row.level_learned,
                    row.machine or "",
                    row.egg_move or ""
                )

        # Stats table
        results_stats_table = self.query_one("#candidate_stats", DataTable)
        results_stats_table.clear()
        if data.stats_table:
            for row in data.stats_table.rows:
                results_stats_table.add_row(
                    row.name,
                    row.attack,
                    row.defense,
                    row.special_attack,
                    row.special_defense,
                    row.speed
                )

        # Types table
        results_types_table = self.query_one("#candidate_types", DataTable)
        results_types_table.clear()
        if data.types_table:
            for row in data.types_table.rows:
                results_types_table.add_row(
                    row.name,
                    row.type1,
                    row.type2 or ""
                )
    
    def compose(self) -> ComposeResult:
        # Checkboxes
        with TabbedContent():
            with TabPane("moves"):
                yield DataTable(id="candidate_moves")
            with TabPane("stats"):
                yield DataTable(id="candidate_stats")
            with TabPane("types"):
                yield DataTable(id="candidate_types")
            with TabPane("type matchups"):
                yield DataTable(id="candidate_type_matchups")

    def on_mount(self) -> None:
        ## Right Pane: Tables - add column headers
        self.query_one("#candidate_moves", DataTable).add_columns(*moves_columns)
        self.query_one("#candidate_stats", DataTable).add_columns(*stats_columns)
        self.query_one("#candidate_types", DataTable).add_columns(*types_columns)
        self.query_one("#candidate_type_matchups", DataTable).add_columns(*type_matchups_columns)