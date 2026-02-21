# Imports
import structlog

from backend.src.lib.repository import JSONRepository

# Schemas
from backend.src.modules.candidate_finder.schemas import (
    CandidateFinderResponse,
    MovesTable,
    MovesTableRow,
    StatsTable,
    StatsTableRow,
    TypesTable,
    TypesTableRow,
)

# Logger
logger = structlog.get_logger(__name__)


class CandidateFinderService:
    def __init__(self, repository: JSONRepository):
        self.repository = repository
        if not self.repository:
            logger.error("Repository not loaded properly")
            raise ValueError("Repository returned empty REPOSITORY object")

    def search_pokemon(
        self,
        move: str | None = None,
        desired_type: str | None = None,
        primary_stat: str | None = None,
        secondary_stat: str | None = None,
        min_primary: int = 0,
        min_secondary: int | None = None,
        min_speed: int | None = None,
        include_legendary: bool = False,
        include_mythical: bool = False,
        include_ultra_beasts: bool = False,
    ) -> frozenset[str]:

        # logger.debug(
        #     "Searching pokemon with:",
        #     move=move,
        #     desired_type=desired_type,
        #     primary_stat=primary_stat,
        #     secondary_stat=secondary_stat,
        #     include_legendary=include_legendary,
        #     include_mythical=include_mythical,
        #     include_ultra_beasts=include_ultra_beasts
        # )

        results = None

        # Apply move filter
        if move:
            move_results = self.repository.get_pokemon_by_move(
                move,
                include_legendary=include_legendary,
                include_mythical=include_mythical,
                include_ultra_beasts=include_ultra_beasts,
            )
            # Convert dict to set of names for intersection
            move_names = frozenset(move_results.keys())
            results = move_names if results is None else results & move_names

        # Apply desired_type filter
        if desired_type:
            type_list = desired_type.split("-")
            type_results = self.repository.get_pokemon_by_type(
                *type_list,
                include_legendary=include_legendary,
                include_mythical=include_mythical,
                include_ultra_beasts=include_ultra_beasts,
            )
            results = type_results if results is None else results & type_results

        # Apply stat filter
        if primary_stat and secondary_stat:
            # try:
            stat_results = self.repository.get_pokemon_by_stats(
                primary_stat,
                secondary_stat,
                min_primary=min_primary,
                min_secondary=min_secondary,
                min_speed=min_speed,
                include_legendary=include_legendary,
                include_mythical=include_mythical,
                include_ultra_beasts=include_ultra_beasts,
            )
            stat_names = frozenset(stat_results.keys())
            results = stat_names if results is None else results & stat_names

        # If no filters applied, raise error
        if results is None:
            logger.warning("No filters provided to search_pokemon")
            raise ValueError("At least one filter parameter is required")

        return results

    def _build_types_table(self, pokemon_names: frozenset[str]) -> TypesTable:
        """Build types table for given Pokemon names."""
        types_rows = []
        for name in sorted(pokemon_names):
            display_name = self.repository.get_pokemon_by_name(name)["display_name"]
            type_display = self.repository.get_pokemon_by_name(name)["type_display"]
            types = type_display.split("/")
            types_rows.append(
                TypesTableRow(name=display_name, type1=types[0], type2=types[1] if len(types) > 1 else None)
            )
        return TypesTable(rows=types_rows)

    def _build_moves_table(self, pokemon_names: frozenset[str], move: str | None = None) -> MovesTable:
        moves_rows = []
        move_index = self.repository.get_move_index()
        machine_moves_index = self.repository.get_machine_moves_index()

        for pokemon_name in sorted(pokemon_names):
            display_name = self.repository.get_pokemon_by_name(pokemon_name)["display_name"]

            # If no move provided, just show pokemon name with empty move info
            if not move:
                moves_rows.append(
                    MovesTableRow(
                        pokemon_name=display_name,
                        move_name="",
                        level_learned="",
                        machine="",
                        egg_move="",
                    )
                )
                continue

            # If move provided but pokemon doesn't learn it, skip
            if move not in move_index or pokemon_name not in move_index[move]:
                continue

            learn_method = move_index[move][pokemon_name]
            level_learned = learn_method.get("level-up") if learn_method.get("level-up") else "x"
            machine = machine_moves_index.get(move) if learn_method.get("machine") else "x"
            egg_move = "yes" if learn_method.get("egg") else "x"

            if level_learned == "x" and machine == "x" and egg_move == "x":
                level_learned = "evolution"

            moves_rows.append(
                MovesTableRow(
                    pokemon_name=display_name,
                    move_name=move,
                    level_learned=level_learned,
                    machine=machine,
                    egg_move=egg_move,
                )
            )
        return MovesTable(rows=moves_rows)

    def _build_stats_table(self, pokemon_names: frozenset[str]) -> StatsTable:
        stats_rows = []
        stat_index = self.repository.get_stat_index()
        for name in sorted(pokemon_names):
            display_name = self.repository.get_pokemon_by_name(name)["display_name"]
            stats = stat_index[name]
            stats_rows.append(
                StatsTableRow(
                    name=display_name,
                    attack=stats["attack"],
                    defense=stats["defense"],
                    special_attack=stats["special_attack"],
                    special_defense=stats["special_defense"],
                    speed=stats["speed"],
                )
            )
        return StatsTable(rows=stats_rows)

    def build_response(self, pokemon_names: frozenset[str], move: str | None) -> CandidateFinderResponse:
        logger.info("Building response tables", count=len(pokemon_names))

        response = CandidateFinderResponse(
            types_table=self._build_types_table(pokemon_names),
            moves_table=self._build_moves_table(pokemon_names, move),
            stats_table=self._build_stats_table(pokemon_names),
        )

        return response
