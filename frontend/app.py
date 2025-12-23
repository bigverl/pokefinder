from textual.app import (
    App, 
    ComposeResult,
    )

from textual.containers import (
    Container,
    Horizontal,
    Vertical,
    VerticalScroll,
    HorizontalGroup,
    VerticalGroup
    )

from textual.suggester import SuggestFromList


from textual.widgets import (
    Header,
    Footer,
    Static,
    Checkbox,
    RadioButton,
    Select,
    Input,
    Label,
    TabbedContent,
    TabPane,
    DataTable,
    Rule,
    Button
    )

# Custom DataTable classes that configure themselves
class MovesDataTable(DataTable):
    pass
    # def on_show(self) -> None:
    #     if self.columns: 
    #         return
    #     self.show_header = True
    #     self.add_columns("level learned", "machine", "egg move")
    #     self.add_row("34", "yes", "no")

class StatsDataTable(DataTable):
    pass
    # def on_show(self) -> None:
    #     if self.columns: 
    #         return
    #     self.show_header = True
    #     self.add_columns("attack", "defense", "special attack", "special defense", "speed")
    #     self.add_row("100", "80", "120", "90", "75")

class TypesDataTable(DataTable):
    pass
    # def on_show(self) -> None:
    #     if self.columns: 
    #         return
    #     self.show_header = True
    #     self.add_columns("type 1", "type 2")
    #     self.add_row("fire", "flying")

class TypeMatchupsDataTable(DataTable):
    pass
    # def on_show(self) -> None:
    #     if self.columns: 
    #         return
    #     self.show_header = True
    #     self.add_columns("4x", "2x", "1x", "0.5x", "0x")
    #     self.add_row("rock", "water, electric", "normal, fighting", "fire, grass", "ground")

"""
Data Table Columns
"""

moves_columns = ["level learned", "machine", "egg move"]

stats_columns = ["attack", "defense", "special attack", "special defense", "speed"]

types_columns = ["type 1", "type 2"]

type_matchups_columns = ["4x", "2x", "1x", "0.5x", "0x"]

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

class Pokefinder(App):
    CSS_PATH = "libs/main.tcss"

    def compose(self) -> ComposeResult:
        # yield Header()
        # Big Box
        with Horizontal(id="app-grid"):
            # Left Pane: Search filters
            with VerticalScroll(id="left-pane", classes="box"):

                # Checkboxes
                with VerticalGroup(id="special_pokemon_box", classes="box"):
                    yield RadioButton("legendary", id="legendary_radio", classes="first-checkbox")
                    yield RadioButton("mythical", id="mythical_radio")
                    yield RadioButton("ultra beast", id="ultra_beast_radio")

                # Move box
                with VerticalGroup(id="move_box", classes="box"):
                    yield RadioButton("enabled", id="move_radio", classes="first-checkbox")
                    with HorizontalGroup(id="move_input_group", classes="boxless_group"):
                       
                        yield Label(id="move_label", content="move name")
                        yield Input(id="move_input", classes="move_input")

                # Stats box
                with VerticalGroup(id="stats_box", classes="box"):
                    # [ ] primary stat: <dropdown>
                    with VerticalGroup(id="stats_enabled_box"):
                        yield RadioButton("enabled", id="primary_stat_radio", classes="first-checkbox")
                    with VerticalGroup(id="primary_stat_box", classes="box"):
                        with HorizontalGroup(id="primary_stat_select_group", classes="box_group"):
                            yield Label(id="primary_stat_label", content="stat name")
                            yield Select(id="primary_stat_select",options=(stat_selections),prompt="select stat")
                        # minimum: <input>
                        with HorizontalGroup(id="primary_stat_input_group", classes="box_group"):
                            yield Label(id="primary_stat_minimum_label", content="minimum value")
                            yield Input(id="primary_stat_input")
                    # secondary stat: <dropdown>
                    with VerticalGroup(id="secondary_stat_box", classes="box"):
                        with HorizontalGroup(id="secondary_stat_filter_group", classes="box_group"):
                            yield Label(id="secondary_stat_label", content="stat name")
                            yield Select(id="secondary_stat_select",options=(stat_selections),prompt="select stat")
                        # minimum: <input>
                        with HorizontalGroup(id="secondary_stat_input_group", classes="box_group"):
                            yield Label(id="secondary_stat_minimum_label", content="minimum value")
                            yield Input(id="secondary_stat_input")                    
                    # minimum speed: <input>
                    with VerticalGroup(id="min_speed_box", classes="box"):
                        with HorizontalGroup(id="min_speed_filter_group", classes="box_group"):
                            yield Label(id="min_speed_label", content="minimum value")
                            yield Input(id="min_speed_stat_input")

                # Desired Type Box
                with VerticalGroup(id="desired_type_box", classes="box"):
                    yield RadioButton("enabled", id="desired_type_radio", classes="first-checkbox")
                    with HorizontalGroup(id="desired_first_type_filter_group", classes="boxless_group"):
                        yield Label(id="desired_first_type_label", content="type 1")
                        yield Input(
                            id="desired_first_type_input",
                            classes="type_input",
                            suggester=SuggestFromList(
                            type_suggestions, case_sensitive=False)
                            )
                    with HorizontalGroup(id="desired_second_type_filter_group", classes="boxless_group"):
                        yield Label(id="desired_second_type_label", content="type 2")
                        yield Input(
                            id="desired_second_type_input",
                            classes="type_input",
                            suggester=SuggestFromList(
                            type_suggestions, case_sensitive=False)
                            )

                # Versus Type Box
                with VerticalGroup(id="versus_type_box", classes="box"):
                    yield RadioButton("enabled", id="versus_type_radio", classes="first-checkbox")
                    with HorizontalGroup(id="versus_first_type_filter_group", classes="boxless_group"):
                        yield Label(id="versus_first_type_label", content="type 1")
                        yield Input(
                            id="desired_first_type_input",
                            classes="type_input",
                            suggester=SuggestFromList(
                            type_suggestions, case_sensitive=False)
                            )
                    with HorizontalGroup(id="versus_second_type_filter_group", classes="boxless_group"):
                        yield Label(id="versus_second_type_label", content="type 2")
                        yield Input(
                            id="versus_second_type_input",
                            classes="type_input",
                            suggester=SuggestFromList(
                            type_suggestions, case_sensitive=False)
                            )
                yield Button(label="Catch 'em all!",classes="go_button")
                        
            # Right Pane: Data tables
            with Vertical(id="right-pane") as right_pane:
                right_pane.border_title = "results"
                with TabbedContent(id="results_tabbedcontent"):
                    with TabPane("moves", id="moves_tabpane"):
                        yield MovesDataTable(id="moves_datatable")
                    with TabPane("stats", id="stats_tabpane"):
                        yield StatsDataTable(id="stats_datatable")
                    with TabPane("types", id="types_tabpane",):
                        yield TypesDataTable(id="types_datatable")
                    with TabPane("type matchups", id="type_matchups_tabpane"):
                        yield TypeMatchupsDataTable(id="type_matchups_datatable")
        yield Footer()

    def on_mount(self) -> None:
        # Border Titles
        self.query_one("#special_pokemon_box", VerticalGroup).border_title = "special pokemon"
        self.query_one("#left-pane").border_title = "poke-finder"
        self.query_one("#move_box").border_title = "move"
        self.query_one("#stats_box").border_title = "stats"
        self.query_one("#primary_stat_box").border_title = "primary stat"
        self.query_one("#secondary_stat_box").border_title = "secondary stat (optional)"
        self.query_one("#min_speed_box").border_title = "desired speed (optional)"
        self.query_one("#desired_type_box").border_title = "desired type"
        self.query_one("#versus_type_box").border_title = "versus type"

        moves = self.query_one("#moves_datatable", MovesDataTable)
        moves.show_header = True
        moves.add_columns("level learned", "machine", "egg move")
        moves.add_row("34", "hm01", "no")
        moves.add_row("18", "tm69", "yes")

        stats = self.query_one("#stats_datatable", StatsDataTable)
        stats.show_header = True
        stats.add_columns("attack", "defense", "special attack", "special defense", "speed")
        stats.add_row("100", "80", "120", "90", "75")

        types = self.query_one("#types_datatable", TypesDataTable)
        types.show_header = True
        types.add_columns("type 1", "type 2")
        types.add_row("fire", "flying")

        matchups = self.query_one("#type_matchups_datatable", TypeMatchupsDataTable)
        matchups.show_header = True
        matchups.add_columns("4x", "2x", "1x", "0.5x", "0x")
        matchups.add_row(
            "rock",
            "water, electric",
            "normal, fighting",
            "fire, grass",
            "ground",
        )

if __name__ == "__main__":
    app = Pokefinder()
    app.run()