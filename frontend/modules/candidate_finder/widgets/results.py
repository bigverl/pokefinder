from typing import TYPE_CHECKING
from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import (
    DataTable,
    TabPane,
    TabbedContent
    )
from textual.widgets.data_table import ColumnKey
from frontend.modules.candidate_finder.schemas import CandidateFinderResponse
import logging

if TYPE_CHECKING:
    from frontend.app import Pokefinder

logger = logging.getLogger(__name__)

"""
Data Table Columns
"""

MOVES_COLUMNS = ["pokemon", "move", "level learned", "machine", "egg move"]

STATS_COLUMNS = ["name", "attack", "defense", "special attack", "special defense", "speed"]

TYPES_COLUMNS = ["name", "type 1", "type 2"]

class CandidateFinderResults(Vertical):
    """
    Left Tab Pane representing candidate finder feature
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Track sort state per table: {table_id: (column_key, reverse)}
        self._sort_state: dict[str, tuple[ColumnKey, bool]] = {}

    @on(DataTable.HeaderSelected)
    def on_header_selected(self, event: DataTable.HeaderSelected) -> None:
        # sort on_click
        table = event.data_table
        column_key = event.column_key
        table_id = table.id
        if table_id is None:
            return

        # get state for this table
        current_col, current_reverse = self._sort_state.get(table_id, (None, False))

        # toggle direction if same column. start ascending (for name)
        if current_col == column_key:
            reverse = not current_reverse
        else:
            reverse = False

        # sort with key function that handles mixed types
        def sort_key(value):
            # If int, return tuple (0, value) so ints sort numerically
            # If str, return tuple (1, value) so strings sort alphabetically
            if isinstance(value, int):
                return (0, value)
            return (1, str(value).lower())

        table.sort(column_key, key=sort_key, reverse=reverse)
        self._sort_state[table_id] = (column_key, reverse)

    # Populate table
    def populate_results_table(self, data: CandidateFinderResponse):
        # Moves table
        results_moves_table = self.query_one("#candidate_moves", DataTable)
        results_moves_table.clear()
        if data.moves_table:
            results_moves_table.add_rows([
                (
                    row.pokemon_name, 
                    row.move_name, 
                    row.level_learned, 
                    row.machine or "", 
                    row.egg_move or ""
                )
                for row in data.moves_table.rows
            ])

        # Stats table
        results_stats_table = self.query_one("#candidate_stats", DataTable)
        results_stats_table.clear()
        if data.stats_table:
            results_stats_table.add_rows([
                (
                    row.name,
                    row.attack,
                    row.defense,
                    row.special_attack,
                    row.special_defense,
                    row.speed)
                    for row in data.stats_table.rows
                
                ])

        # Types table
        results_types_table = self.query_one("#candidate_types", DataTable)
        results_types_table.clear()
        if data.types_table:
            results_types_table.add_rows([
                (
                    row.name,
                    row.type1,
                    row.type2 or ""
                    )
                    for row in data.types_table.rows
                ])
    
    def compose(self) -> ComposeResult:
        # Checkboxes
        with TabbedContent():
            with TabPane("moves"):
                yield DataTable(id="candidate_moves")
            with TabPane("stats"):
                yield DataTable(id="candidate_stats")
            with TabPane("types"):
                yield DataTable(id="candidate_types")

    def on_mount(self) -> None:
        ## Right Pane: Tables - add column headers
        self.query_one("#candidate_moves", DataTable).add_columns(*MOVES_COLUMNS)
        self.query_one("#candidate_stats", DataTable).add_columns(*STATS_COLUMNS)
        self.query_one("#candidate_types", DataTable).add_columns(*TYPES_COLUMNS)