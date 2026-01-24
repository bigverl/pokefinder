
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


class PokedexResults(Vertical):
    """
    Left Tab Pane representing candidate finder feature
    """
    
    def compose(self) -> ComposeResult:

        # Checkboxes
        with TabbedContent():
            with TabPane("summary"):
                yield DataTable(id="pokemon_summary")
            with TabPane("base stats"):
                yield DataTable(id="base_stats")
            with TabPane("moves"):
                yield DataTable(id="pokemon_moves")

    def on_mount(self) -> None:
        pass


