

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

class CoverageAnalyzerResults(Vertical):
    """
    Left Tab Pane representing candidate finder feature
    """
    
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("strengths"):
                yield DataTable(id="coverage_strengths")
            with TabPane("weaknesses"):
                yield DataTable(id="coverage_weaknesses")
            with TabPane("suggested types"):
                yield DataTable(id="coverage_suggested_types")
    
    def on_mount(self) -> None:
        pass




