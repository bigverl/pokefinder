

from textual.app import ComposeResult

from textual.containers import (
    Vertical,
    HorizontalGroup,
    VerticalGroup
    )

from textual.suggester import SuggestFromList

from textual.widgets import (
    Input,
    Label,
    Button,
    RadioButton
    )

type_suggestions = [
    "normal", "fire", "water", "electric", "grass", "ice",
    "fighting", "poison", "ground", "flying", "psychic", "bug",
    "rock", "ghost", "dragon", "dark", "steel", "fairy"
]

class CoverageAnalyzerSearch(Vertical):

    def compose(self) -> ComposeResult:
        yield Label(content="Type")

        # Checkboxes
        with VerticalGroup(id="special_pokemon_box", classes="box"):
            yield RadioButton("legendary")
            yield RadioButton("mythical")
            yield RadioButton("ultra beast")

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
                
        yield Button(label="Scan", classes="go_button")  
    
    def on_mount(self) -> None:
        pass




