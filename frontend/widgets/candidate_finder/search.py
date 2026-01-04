from typing import TYPE_CHECKING
from textual import on
from textual.app import ComposeResult

from textual.containers import (
    HorizontalGroup,
    VerticalGroup,
    Vertical
    )

from textual.suggester import SuggestFromList

from textual.widgets import (
    RadioButton,
    Select,
    Input,
    Label,
    Button
    )

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
    
    def compose(self) -> ComposeResult:

        # Checkboxes
        with VerticalGroup(id="special_pokemon_box", classes="box"):
            yield RadioButton("legendary")
            yield RadioButton("mythical")
            yield RadioButton("ultra beast")

        # Move box
        with VerticalGroup(id="move_box", classes="box"):
            yield RadioButton("enabled")
            with HorizontalGroup(classes="aligned_inputs"):
                yield Label(content="move name")
                yield Input()

        # Stats box
        with VerticalGroup(id="stats_box", classes="box"):
            # [ ] primary stat: <dropdown>
            with VerticalGroup():
                yield RadioButton("enabled")
            with VerticalGroup(id="primary_stat_box", classes="box"):
                # statname: <select>
                with HorizontalGroup():
                    yield Label(content="stat name")
                    yield Select(prompt="select stat",options=(stat_selections))
                # minimum: <input>
                with HorizontalGroup():
                    yield Label(content="minimum value")
                    yield Input()
                # statname: <select>
            with VerticalGroup(id="secondary_stat_box", classes="box"):
                with HorizontalGroup():
                    yield Label(content="stat name")
                    yield Select(prompt="select stat", options=(stat_selections))
                # minimum: <input>
                with HorizontalGroup():
                    yield Label(content="minimum value")
                    yield Input()                    
            # minimum speed: <input>
            with VerticalGroup(id="min_speed_box", classes="box"):
                with HorizontalGroup():
                    yield Label(content="minimum value")
                    yield Input()

        # Desired Type Box
        with VerticalGroup(id="desired_type_box", classes="box"):
            yield RadioButton("enabled")
            with HorizontalGroup(classes="aligned_inputs"):
                yield Label(content="type 1")
                yield Input(
                    classes="type_input",
                    suggester=SuggestFromList(
                    type_suggestions, case_sensitive=False)
                    )
            with HorizontalGroup(classes="aligned_inputs"):
                yield Label(content="type 2")
                yield Input(
                    classes="type_input",
                    suggester=SuggestFromList(
                    type_suggestions, case_sensitive=False)
                    )

        # Versus Type Box
        with VerticalGroup(id="versus_type_box", classes="box"):
            yield RadioButton("enabled")
            with HorizontalGroup(classes="aligned_inputs"):
                yield Label(content="type 1")
                yield Input(
                    classes="type_input",
                    suggester=SuggestFromList(
                    type_suggestions, case_sensitive=False)
                    )
            with HorizontalGroup(classes="aligned_inputs"):
                yield Label(content="type 2")
                yield Input(
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
            self.query_one("#versus_type_box").border_title = "versus type"
        except Exception as e:
            self.notify(f"MOUNT ERROR: {str(e)}", severity="error", timeout=30)
            self.log.error(f"Exception in on_mount: {e}")