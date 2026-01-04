from typing import TYPE_CHECKING
from textual import on
from textual.app import ComposeResult

from textual.containers import (
    Vertical
    )


from textual.widgets import (
    DataTable,
    TabPane,
    TabbedContent
    )

if TYPE_CHECKING:
    from frontend.app import Pokefinder

"""
Data Table Columns
"""

moves_columns = ["name", "level learned", "machine", "egg move"]

stats_columns = ["name", "attack", "defense", "special attack", "special defense", "speed"]

types_columns = ["name", "type 1", "type 2"]

type_matchups_columns = ["type combo", "4x", "2x", "1x", "0.5x", "0x"]

class CandidateFinderResults(Vertical):
    """
    Left Tab Pane representing candidate finder feature
    """
    
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
        ## Right Pane: Tables
        try:
            moves = self.query_one("#candidate_moves", DataTable)
            moves.add_columns(*moves_columns)
            moves.add_row("pikachu", "34", "hm01", "no")
            moves.add_row("pikachu", "18", "tm69", "yes")
        except Exception as e:
            self.notify(f"MOUNT ERROR: {str(e)}", severity="error", timeout=30)
            self.log.error(f"Exception in on_mount: {e}")

        try:
            stats = self.query_one("#candidate_stats", DataTable)
            stats.add_columns(*stats_columns)
            stats.add_row("charizard", "100", "80", "120", "90", "75")
        except Exception as e:
            self.notify(f"MOUNT ERROR: {str(e)}", severity="error", timeout=30)
            self.log.error(f"Exception in on_mount: {e}")

        try:
            types = self.query_one("#candidate_types", DataTable)
            types.add_columns(*types_columns)
            types.add_row("moltres", "fire", "flying")
        except Exception as e:
            self.notify(f"MOUNT ERROR: {str(e)}", severity="error", timeout=30)
            self.log.error(f"Exception in on_mount: {e}")

        try:
            matchups = self.query_one("#candidate_type_matchups", DataTable)
            matchups.add_columns(*type_matchups_columns)
            matchups.add_row(
                "fire/flying",
                "rock",
                "water, electric",
                "normal, fighting",
                "fire, grass",
                "ground",
            )
        except Exception as e:
            self.notify(f"MOUNT ERROR: {str(e)}", severity="error", timeout=30)
            self.log.error(f"Exception in on_mount: {e}")