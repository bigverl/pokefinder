from textual.app import ComposeResult
from textual.containers import HorizontalGroup, Vertical, VerticalGroup
from textual.suggester import SuggestFromList
from textual.widgets import Button, Input, Label, RadioButton

TYPE_SUGGESTIONS = [
    "normal",
    "fire",
    "water",
    "electric",
    "grass",
    "ice",
    "fighting",
    "poison",
    "ground",
    "flying",
    "psychic",
    "bug",
    "rock",
    "ghost",
    "dragon",
    "dark",
    "steel",
    "fairy",
]


class CoverageAnalyzerSearch(Vertical):
    def _collect_search_params(self) -> list[str]:
        """Collect enabled slots into a list of type combo strings."""
        slots = []
        for i in range(1, 7):
            radio = self.query_one(f"#slot_{i}_radio", RadioButton)
            if radio.value:
                type1 = self.query_one(f"#slot_{i}_type1", Input).value.strip().lower()
                type2 = self.query_one(f"#slot_{i}_type2", Input).value.strip().lower()
                if type1:
                    combo = f"{type1}-{type2}" if type2 else type1
                    slots.append(combo)
        return slots

    def compose(self) -> ComposeResult:
        for i in range(1, 7):
            with VerticalGroup(id=f"slot_{i}_box", classes="box"):
                yield RadioButton("enabled", id=f"slot_{i}_radio")
                with HorizontalGroup(classes="aligned_inputs"):
                    yield Label(content="type 1")
                    yield Input(
                        id=f"slot_{i}_type1",
                        classes="type_input",
                        suggester=SuggestFromList(TYPE_SUGGESTIONS, case_sensitive=False),
                    )
                with HorizontalGroup(classes="aligned_inputs"):
                    yield Label(content="type 2")
                    yield Input(
                        id=f"slot_{i}_type2",
                        classes="type_input",
                        suggester=SuggestFromList(TYPE_SUGGESTIONS, case_sensitive=False),
                    )

        yield Button(label="Scan", classes="go_button scan_button")

    def on_mount(self) -> None:
        for i in range(1, 7):
            try:
                self.query_one(f"#slot_{i}_box", VerticalGroup).border_title = f"slot {i}"
            except Exception as e:
                self.notify(f"MOUNT ERROR: {str(e)}", severity="error", timeout=30)
                self.log.error(f"Exception in on_mount: {e}")
