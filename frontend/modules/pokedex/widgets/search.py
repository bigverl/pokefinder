from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label


class PokedexSearch(Vertical):
    """
    Left Tab Pane representing pokedex feature
    """

    def compose(self) -> ComposeResult:
        yield Label(content="Pokedex")

    def on_mount(self) -> None:
        pass
