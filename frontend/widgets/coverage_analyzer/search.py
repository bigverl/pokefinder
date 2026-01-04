

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

class CoverageAnalyzerSearch(Vertical):
    """
    Left Tab Pane representing candidate finder feature
    """
    
    def compose(self) -> ComposeResult:
        yield Label(content="Type")
        yield Button(label="Scan", classes="go_button")  
    
    def on_mount(self) -> None:
        pass




