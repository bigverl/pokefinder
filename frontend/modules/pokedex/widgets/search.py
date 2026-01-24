from typing import TYPE_CHECKING
from textual import on
from textual.app import ComposeResult

from textual.containers import (
    Vertical
    )

from textual.widgets import (
    Select,
    Input,
    Label,
    Button
    )

class PokedexSearch(Vertical):
    """
    Left Tab Pane representing pokedex feature
    """
    
    def compose(self) -> ComposeResult:
        yield Label(content="Pokedex")
    
    def on_mount(self) -> None:
        pass
