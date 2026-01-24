# Imports
import structlog

from typing import Any

from backend.src.lib.repository import SQLAlchemyRepository

# Schemas
from backend.src.modules.candidate_finder.schemas import (
    CandidateFinderResponse,
    MovesTable,
    MovesTableRow,
    StatsTable,
    StatsTableRow,
    TypesTable,
    TypesTableRow
)

# Logger
logger = structlog.get_logger(__name__)

class CandidateFinderService():

    def __init__(self, repository: SQLAlchemyRepository):
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
        include_ultra_beasts: bool = False
    ) -> frozenset[str]:
        """
        Search for Pokemon using multiple filters combined with AND logic.

        All provided filters are combined - Pokemon must match ALL criteria.

        Args:
            move: Move name filter
            desired_type: Desired Pokemon type filter (e.g., "fire" or "fire-flying")
            primary_stat: Primary stat for stat search
            secondary_stat: Secondary stat for stat search
            min_primary: Minimum primary stat value
            min_secondary: Minimum secondary stat value
            min_speed: Minimum speed value
            include_legendary: Include legendary Pokemon
            include_mythical: Include mythical Pokemon
            include_ultra_beasts: Include Ultra Beasts

        Returns:
            frozenset of Pokemon names matching all filters
        """
        logger.debug(
            "Searching pokemon with:",
            move=move,
            desired_type=desired_type,
            primary_stat=primary_stat,
            secondary_stat=secondary_stat,
            include_legendary=include_legendary,
            include_mythical=include_mythical,
            include_ultra_beasts=include_ultra_beasts
        )

        results = None

        # Apply move filter
        if move:
            move_results = self.repository.get_pokemon_by_move(
                move,
                include_legendary=include_legendary,
                include_mythical=include_mythical,
                include_ultra_beasts=include_ultra_beasts
            )
            # Convert dict to set of names for intersection
            move_names = frozenset(move_results.keys())
            results = move_names if results is None else results & move_names

        # Apply desired_type filter
        if desired_type:
            type_list = desired_type.split('-')
            type_results = self.repository.get_pokemon_by_type(
                *type_list,
                include_legendary=include_legendary,
                include_mythical=include_mythical,
                include_ultra_beasts=include_ultra_beasts
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
                include_ultra_beasts=include_ultra_beasts
                
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
            # Get type
            pokemon_types = []
            type_index = self.repository.get_type_index()
            for type_name, pokemon_set in type_index.items():
                if name in pokemon_set:
                    pokemon_types.append(type_name)

            types_rows.append(TypesTableRow(
                name=name,
                type1=pokemon_types[0],
                type2=pokemon_types[1] if len(pokemon_types) > 1 else None
            ))
        return TypesTable(rows=types_rows)

    def _build_moves_table(self, pokemon_names: frozenset[str]) -> MovesTable:
        """Build moves table for given Pokemon names."""
        moves_rows = []
        move_index = self.repository.get_move_index()
        machine_moves_index = self.repository.get_machine_moves_index()
        for pokemon_name in sorted(pokemon_names):
            # get all moves for this Pokemon from the moves index

            for move_name, learners in move_index.items():
                if pokemon_name in learners:
                    learn_method = learners[pokemon_name]
                    
                    # set move categories
                    level_learned = learn_method.get("level-up") if learn_method.get("level-up") else "x"
                    machine = machine_moves_index.get(move_name) if learn_method.get("machine") else "x"
                    egg_move = "yes" if learn_method.get("egg") else "x"

                    # catch evolution move data error
                    if level_learned == "x" and machine == "x" and egg_move == "x":
                        level_learned = "evolution"

                    # insert row
                    moves_rows.append(MovesTableRow(
                        pokemon_name=pokemon_name,
                        move_name=move_name,
                        level_learned=level_learned,
                        machine=machine,
                        egg_move= egg_move,
                    ))
        return MovesTable(rows=moves_rows)

    def _build_stats_table(self, pokemon_names: frozenset[str]) -> StatsTable:
        """Build stats table for given Pokemon names."""
        stats_rows = []
        stat_index = self.repository.get_stat_index()
        for name in sorted(pokemon_names):
            stats = stat_index[name]
            stats_rows.append(StatsTableRow(
                name=name,
                attack=stats["attack"],
                defense=stats["defense"],
                special_attack=stats["special_attack"],
                special_defense=stats["special_defense"],
                speed=stats["speed"]
            ))
        return StatsTable(rows=stats_rows)


    def build_response(self, pokemon_names: frozenset[str]) -> CandidateFinderResponse:
        """Build full CandidateFinderResponse with all tables populated."""
        logger.info("Building response tables", count=len(pokemon_names))

        return CandidateFinderResponse(
            types_table=self._build_types_table(pokemon_names),
            moves_table=self._build_moves_table(pokemon_names),
            stats_table=self._build_stats_table(pokemon_names),
        )