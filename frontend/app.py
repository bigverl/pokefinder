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
    Footer,
    TabbedContent,
    TabPane,
    )

from frontend.widgets.candidate_finder.search import CandidateFinderSearch
from frontend.widgets.candidate_finder.results import CandidateFinderResults

from frontend.widgets.pokedex.search import PokedexSearch
from frontend.widgets.pokedex.results import PokedexResults

from frontend.widgets.coverage_analyzer.search import CoverageAnalyzerSearch
from frontend.widgets.coverage_analyzer.results import CoverageAnalyzerResults

from frontend.libs.feature_flags import FEATURE_FLAGS

class Pokefinder(App):
    CSS_PATH = "libs/main.tcss"

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

if __name__ == "__main__":
    app = Pokefinder()
    app.run()