from textual.app import (
    App, 
    ComposeResult,
    )

from textual import on, log

from textual.containers import (
    Horizontal,
    Vertical,
    VerticalScroll,
    )

from textual.widgets import (
    Button,
    Footer,
    TabbedContent,
    TabPane,
    )

from frontend.api_client import BackendClient

from frontend.modules.candidate_finder.widgets.search import CandidateFinderSearch
from frontend.modules.candidate_finder.widgets.results import CandidateFinderResults

from frontend.modules.pokedex.widgets.search import PokedexSearch
from frontend.modules.pokedex.widgets.results import PokedexResults

from frontend.modules.coverage_analyzer.widgets.search import CoverageAnalyzerSearch
from frontend.modules.coverage_analyzer.widgets.results import CoverageAnalyzerResults

from frontend.libs.feature_flags import FEATURE_FLAGS

class Pokefinder(App):
    CSS_PATH = "libs/main.tcss"

    def __init__(self):
        super().__init__()
        self.api_client = BackendClient()

    def compose(self) -> ComposeResult:
        with Horizontal():
            # Left Pane: Feature Selector / Search Panel
            with VerticalScroll(id="left_pane", classes="box") as left_pane:
                left_pane.border_title = "poke-finder"
                with TabbedContent(id="mode_tabs"):
                    with TabPane("candidate finder", id="candidate_search", classes="feature_tabs"):
                        yield CandidateFinderSearch()
                    if FEATURE_FLAGS.pokedex:
                        with TabPane("pokedex", id="pokedex_search"):
                            yield PokedexSearch()
                    if FEATURE_FLAGS.coverage_analyzer:
                        with TabPane("type coverage", id="coverage_search"):
                            yield CoverageAnalyzerSearch()
            # Right Pane: Results Panel
            with Vertical(id="right_pane") as right_pane:
                right_pane.border_title = "results"
                yield CandidateFinderResults(id="candidate_results", classes="results_tabs")
                if FEATURE_FLAGS.pokedex:
                    yield PokedexResults(id="pokedex_results", classes="results_tabs hidden")
                if FEATURE_FLAGS.coverage_analyzer:
                    yield CoverageAnalyzerResults(id="coverage_results", classes="results_tabs hidden")
        yield Footer()

    @on(TabbedContent.TabActivated, selector="#mode_tabs")
    def mode_changed(self, event: TabbedContent.TabActivated) -> None:
        # Hide all result tabs
        for tabs in self.query(".results_tabs"):
            tabs.add_class("hidden")

        # Show the one matching current mode
        if event.pane.id == "candidate_search":
            self.query_one("#candidate_results").remove_class("hidden")
        elif event.pane.id == "pokedex_search":
            self.query_one("#pokedex_results").remove_class("hidden")
        elif event.pane.id == "coverage_search":
            self.query_one("#coverage_results").remove_class("hidden")

    def on_mount(self) -> None:
        pass

    # ===================
    # Candidate Finder
    # ===================

    @on(Button.Pressed, ".go_button")
    async def on_candidate_finder_search(self, event: Button.Pressed) -> None:
        search_widget = self.query_one(CandidateFinderSearch)
        try:
            params = search_widget._collect_search_params()
            response = await self.api_client.search_pokemon(**params)
            results_widget = self.query_one(CandidateFinderResults)
            results_widget.populate_results_table(response)
        except ValueError as e:
            self.notify(str(e), severity="error")
        except Exception as e:
            self.notify(f"Search failed: {e}", severity="error")

if __name__ == "__main__":
    app = Pokefinder()
    app.run()