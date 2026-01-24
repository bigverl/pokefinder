from typing import TYPE_CHECKING
from textual import on
from textual.app import ComposeResult

from textual.containers import (
    HorizontalGroup,
    VerticalGroup,
    Vertical
    )

from textual.widgets import (
    RadioButton,
    Select,
    Input,
    Label,
    Button
    )

from textual.suggester import SuggestFromList

if TYPE_CHECKING:
    from frontend.app import Pokefinder


type_selections = [
    ("normal", "normal"),
    ("fire", "fire"),
    ("water", "water"),
    ("electric", "electric"),
    ("grass", "grass"),
    ("ice", "ice"),
    ("fighting", "fighting"),
    ("poison", "poison"),
    ("ground", "ground"),
    ("flying", "flying"),
    ("psychic", "psychic"),
    ("bug", "bug"),
    ("rock", "rock"),
    ("ghost", "ghost"),
    ("dragon", "dragon"),
    ("dark", "dark"),
    ("steel", "steel"),
    ("fairy", "fairy")
    ]

type_suggestions = [
    "normal", "fire", "water", "electric", "grass", "ice",
    "fighting", "poison", "ground", "flying", "psychic", "bug",
    "rock", "ghost", "dragon", "dark", "steel", "fairy"
]

stat_selections = [
    ("attack","attack"),
    ("defense","defense"),
    ("special attack","special_attack"),
    ("special defense","special_defense"),
    ("speed","speed")
    ]


class CandidateFinderSearch(Vertical):
    """
    Left Tab Pane representing candidate finder feature
    """

    def _parse_int(self, value: str) -> int | None:
        """Parse string to int, rejecting floats."""
        if not value:
            return None
        if "." in value:
            raise ValueError(f"Expected integer, got float: {value}")
        return int(value)

    def _collect_search_params(self):
        move_enabled = self.query_one("#move_radio_button", RadioButton).value
        stats_enabled = self.query_one("#stats_radio_button", RadioButton).value
        desired_type_enabled = self.query_one("#desired_type_radio_button", RadioButton).value

        desired_type = ""
        if desired_type_enabled:
            type1 = self.query_one("#type1_input", Input).value
            type2 = self.query_one("#type2_input", Input).value
            desired_type = f"{type1}-{type2}" if type2 else type1

        params = {
            "move": self.query_one("#move_input", Input).value if move_enabled else None,
            "desired_type": desired_type if desired_type_enabled else None,
            "primary_stat": self.query_one("#primary_stat_select", Select).value if stats_enabled else None,
            "secondary_stat":  self.query_one("#secondary_stat_select", Select).value if stats_enabled else None,
            "min_primary": self._parse_int(self.query_one("#primary_stat_input", Input).value) if stats_enabled else None,
            "min_secondary": self._parse_int(self.query_one("#secondary_stat_input", Input).value) if stats_enabled else None,
            "min_speed": self._parse_int(self.query_one("#speed_input", Input).value) if stats_enabled else None,
            "include_mythical": self.query_one("#mythical_radio_button", RadioButton).value,
            "include_legendary": self.query_one("#legendary_radio_button", RadioButton).value,
            "include_ultra_beasts": self.query_one("#ultra_beast_radio_button", RadioButton).value,
        }

        return params


    def compose(self) -> ComposeResult:

        # Checkboxes
        with VerticalGroup(id="special_pokemon_box", classes="box"):
            yield RadioButton("legendary", id="legendary_radio_button")
            yield RadioButton("mythical", id="mythical_radio_button")
            yield RadioButton("ultra beast", id="ultra_beast_radio_button")

        # Move box
        with VerticalGroup(id="move_box", classes="box"):
            yield RadioButton("enabled", id="move_radio_button")
            with HorizontalGroup(classes="aligned_inputs"):
                yield Label(content="move name")
                yield Input(id="move_input")

        # Stats box
        with VerticalGroup(id="stats_box", classes="box"):
            # [ ] primary stat: <dropdown>
            with VerticalGroup():
                yield RadioButton("enabled", id="stats_radio_button")
            with VerticalGroup(id="primary_stat_box", classes="box"):
                # statname: <select>
                with HorizontalGroup():
                    yield Label(content="stat name")
                    yield Select(
                        prompt="select stat",
                        options=(stat_selections),
                        id="primary_stat_select")
                # minimum: <input>
                with HorizontalGroup():
                    yield Label(content="minimum value")
                    yield Input(id="primary_stat_input")
                # statname: <select>
            with VerticalGroup(id="secondary_stat_box", classes="box"):
                with HorizontalGroup():
                    yield Label(content="stat name")
                    yield Select(
                        prompt="select stat",
                        options=(stat_selections),
                        id="secondary_stat_select")
                # minimum: <input>
                with HorizontalGroup():
                    yield Label(content="minimum value")
                    yield Input(id="secondary_stat_input")
            # minimum speed: <input>
            with VerticalGroup(id="min_speed_box", classes="box"):
                with HorizontalGroup():
                    yield Label(content="minimum value")
                    yield Input(id="speed_input")

        # Desired Type Box
        with VerticalGroup(id="desired_type_box", classes="box"):
            yield RadioButton("enabled",id="desired_type_radio_button")
            with HorizontalGroup(classes="aligned_inputs"):
                yield Label(content="type 1")
                yield Input(
                    id="type1_input",
                    classes="type_input",
                    suggester=SuggestFromList(
                    type_suggestions, case_sensitive=False)
                    )
            with HorizontalGroup(classes="aligned_inputs"):
                yield Label(content="type 2")
                yield Input(
                    id="type2_input",
                    classes="type_input",
                    suggester=SuggestFromList(
                    type_suggestions, case_sensitive=False)
                    )

        yield Button(label="Catch 'em all!", classes="go_button")


    def on_mount(self) -> None:

        ## Left Pane: Border titles
        try:
            self.query_one("#special_pokemon_box", VerticalGroup).border_title = "special pokemon"
            self.query_one("#move_box").border_title = "move"
            self.query_one("#stats_box").border_title = "stats"
            self.query_one("#primary_stat_box").border_title = "primary stat"
            self.query_one("#secondary_stat_box").border_title = "secondary stat (optional)"
            self.query_one("#min_speed_box").border_title = "desired speed (optional)"
            self.query_one("#desired_type_box").border_title = "desired type"
        except Exception as e:
            self.notify(f"MOUNT ERROR: {str(e)}", severity="error", timeout=30)
            self.log.error(f"Exception in on_mount: {e}")
