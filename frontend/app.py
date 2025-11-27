"""
Pokedex TUI Application
A terminal-based Pokédex using Textual framework with three-panel layout.
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import ListView, ListItem, Static, Label
from textual.binding import Binding
# from textual.messages import work

import api.client as client


class PokemonList(ListView):
    """Left panel: List of Pokemon (15% width)."""
    
    BINDINGS = [
        Binding("up", "cursor_up", "Move Up", show=False),
        Binding("down", "cursor_down", "Move Down", show=False),
        Binding("left", "page_up", "Previous Page", show=False),
        Binding("right", "page_down", "Next Page", show=False),
        Binding("enter", "select_pokemon", "Select", show=False),
    ]
    
    def on_mount(self) -> None:
        """Populate with stub Pokemon data on startup."""
        # TODO: Replace with actual API call to pokeapi.co
        stub_pokemon = [
            "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon",
            "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie",
            "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill",
            "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate"
        ]
        
        for pokemon in stub_pokemon:
            self.append(ListItem(Label(pokemon)))
    
    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """When cursor hovers over a Pokemon, update center panel."""
        if event.item:
            label = event.item.children[0]
            pokemon_name = label.render()
            self.app.update_pokemon_info(str(pokemon_name))
    
    def action_page_up(self) -> None:
        """Page up through the list (left key)."""
        visible_items = 10  # Approximate items visible at once
        current = self.index or 0
        new_index = max(0, current - visible_items)
        self.index = new_index
    
    def action_page_down(self) -> None:
        """Page down through the list (right key)."""
        visible_items = 10
        current = self.index or 0
        new_index = min(len(self.children) - 1, current + visible_items)
        self.index = new_index
    
    def action_select_pokemon(self) -> None:
        """Enter key opens the details menu on the right."""
        self.app.show_details_menu()


class PokemonInfo(Static):
    """Center panel: Pokemon information display (70% width)."""
    
    def on_mount(self) -> None:
        """Initialize with placeholder content."""
        self.update("[dim]Select a Pokemon to view details[/dim]")
    
    # @work(exclusive=True)
    async def display_pokemon(self, name: str) -> None:
        """Display Pokemon information.
        
        Args:
            name: Pokemon name to display
        """
        # TODO: Fetch actual data from pokeapi.co/api/v2/pokemon/{name}
        # TODO: Parse and format: name, types, abilities, stats, sprites, etc.
     
        await client.get_pokemon("ditto")

        pokemon_data = self.worker.wait()
        log(pokemon_data)

        self.update(pokemon_data)
#         self.update(f"""
# [bold cyan]{name.upper()}[/bold cyan]

# [yellow]Type:[/yellow] TODO - Fetch from API
# [yellow]Height:[/yellow] TODO - Fetch from API
# [yellow]Weight:[/yellow] TODO - Fetch from API

# [yellow]Abilities:[/yellow]
#   • TODO - Fetch from API
#   • TODO - Fetch from API

# [yellow]Base Stats:[/yellow]
#   HP: TODO
#   Attack: TODO
#   Defense: TODO
#   Sp. Atk: TODO
#   Sp. Def: TODO
#   Speed: TODO

# [dim]Press ENTER to see more details[/dim]
#         """)
    
    def display_detail_view(self, detail_type: str, pokemon_name: str) -> None:
        """Display specific detail view based on menu selection.
        
        Args:
            detail_type: Type of detail to show ('detail', 'strengths', 'initial moves')
            pokemon_name: Pokemon to show details for
        """
        # TODO: Implement different views based on detail_type
        # TODO: Fetch appropriate data from pokeapi.co
        if detail_type == "Detail":
            content = f"[bold]Full Details for {pokemon_name}[/bold]\n\nTODO: Species info, evolution chain, etc."
        elif detail_type == "Strengths":
            content = f"[bold]Type Effectiveness for {pokemon_name}[/bold]\n\nTODO: Strong against, weak against"
        elif detail_type == "Initial Moves":
            content = f"[bold]Starting Moves for {pokemon_name}[/bold]\n\nTODO: Level 1 moves, learned moves"
        else:
            content = "Unknown detail type"
        
        self.update(content)


class DetailsMenu(ListView):
    """Right panel: Pokemon details submenu (15% width)."""
    
    BINDINGS = [
        Binding("up", "cursor_up", "Move Up", show=False),
        Binding("down", "cursor_down", "Move Down", show=False),
        Binding("enter", "select_detail", "Select Detail", show=False),
        Binding("escape", "close_menu", "Close Menu", show=False),
    ]
    
    def on_mount(self) -> None:
        """Populate menu options."""
        options = ["Detail", "Strengths", "Initial Moves"]
        for option in options:
            self.append(ListItem(Label(option)))
        
    def action_select_detail(self) -> None:
            """Enter key on a menu item updates the center panel."""
            if self.highlighted_child:
                label = self.highlighted_child.children[0]
                detail_type = str(label.render())
                self.app.show_detail_view(detail_type)
                
    def action_close_menu(self) -> None:
        """Escape key closes the menu and returns focus to Pokemon list."""
        self.app.hide_details_menu()


class PokedexApp(App):
    """Main Pokedex TUI Application."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    Horizontal {
        height: 100%;
    }
    
    PokemonList {
        width: 15%;
        border: solid $primary;
        padding: 1;
    }
    
    PokemonInfo {
        width: 70%;
        border: solid $primary;
        padding: 1;
    }
    
    DetailsMenu {
        width: 15%;
        border: solid $accent;
        padding: 1;
    }
    
    .hidden {
        display: none;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]
    
    def __init__(self):
        super().__init__()
        self.current_pokemon = None
        self.details_visible = False
    
    def compose(self) -> ComposeResult:
        """Create the three-panel layout."""
        with Horizontal():
            yield PokemonList()
            yield PokemonInfo()
            yield DetailsMenu().add_class("hidden")  # Hidden by default
    
    def update_pokemon_info(self, pokemon_name: str) -> None:
        """Update center panel when hovering over a Pokemon.
        
        Args:
            pokemon_name: Name of the Pokemon to display
        """
        self.current_pokemon = pokemon_name
        info_panel = self.query_one(PokemonInfo)
        info_panel.display_pokemon(pokemon_name)
    
    def show_details_menu(self) -> None:
        """Show the details menu and shift focus to it (Enter key on Pokemon)."""
        if not self.details_visible:
            menu = self.query_one(DetailsMenu)
            menu.remove_class("hidden")
            menu.focus()
            self.details_visible = True
    
    def hide_details_menu(self) -> None:
        """Hide the details menu and return focus to Pokemon list (Escape key)."""
        if self.details_visible:
            menu = self.query_one(DetailsMenu)
            menu.add_class("hidden")
            
            pokemon_list = self.query_one(PokemonList)
            pokemon_list.focus()
            self.details_visible = False
    
    def show_detail_view(self, detail_type: str) -> None:
        """Display specific detail view in center panel.
        
        Args:
            detail_type: Type of detail selected from menu
        """
        if self.current_pokemon:
            info_panel = self.query_one(PokemonInfo)
            info_panel.display_detail_view(detail_type, self.current_pokemon)


if __name__ == "__main__":
    app = PokedexApp()
    app.run()
