from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import DataTable, TabbedContent, TabPane
from textual.widgets.data_table import ColumnKey

from frontend.modules.coverage_analyzer.schemas import CoverageAnalyzerResponse

COVERAGE_COLUMNS = ["effectiveness", "enemy type", "your type"]


class CoverageAnalyzerResults(Vertical):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sort_state: dict[str, tuple[ColumnKey, bool]] = {}

    @on(DataTable.HeaderSelected)
    def on_header_selected(self, event: DataTable.HeaderSelected) -> None:
        table = event.data_table
        column_key = event.column_key
        table_id = table.id
        if table_id is None:
            return

        current_col, current_reverse = self._sort_state.get(table_id, (None, False))

        if current_col == column_key:
            reverse = not current_reverse
        else:
            reverse = False

        def sort_key(value):
            if isinstance(value, int):
                return (0, value)
            return (1, str(value).lower())

        table.sort(column_key, key=sort_key, reverse=reverse)
        self._sort_state[table_id] = (column_key, reverse)

    def populate_results_table(self, data: CoverageAnalyzerResponse):
        # Strengths table
        strengths_table = self.query_one("#coverage_strengths", DataTable)
        strengths_table.clear()
        if data.team_strengths_table:
            strengths_table.add_rows(
                [
                    (
                        row.effectiveness,
                        row.enemy_type,
                        row.friendly_type,
                    )
                    for row in data.team_strengths_table.rows
                ]
            )

        # Weaknesses table
        weaknesses_table = self.query_one("#coverage_weaknesses", DataTable)
        weaknesses_table.clear()
        if data.team_weaknesses_table:
            weaknesses_table.add_rows(
                [
                    (
                        row.effectiveness,
                        row.enemy_type,
                        row.friendly_type,
                    )
                    for row in data.team_weaknesses_table.rows
                ]
            )

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("strengths"):
                yield DataTable(id="coverage_strengths")
            with TabPane("weaknesses"):
                yield DataTable(id="coverage_weaknesses")

    def on_mount(self) -> None:
        self.query_one("#coverage_strengths", DataTable).add_columns(*COVERAGE_COLUMNS)
        self.query_one("#coverage_weaknesses", DataTable).add_columns(*COVERAGE_COLUMNS)
