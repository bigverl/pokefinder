import structlog

from backend.src.lib.repository import SQLAlchemyRepository

# Schemas
from backend.src.modules.coverage_analyzer.schemas import (
    CoverageAnalyzerResponse,
    TypeCoverageTable,
    TypeCoverageTableRow,
)

# Logger
logger = structlog.get_logger(__name__)


class CoverageAnalyzerService:
    def __init__(self, repository: SQLAlchemyRepository):
        self.repository = repository
        if not self.repository:
            logger.error("Repository not loaded properly")
            raise ValueError("Repository returned empty REPOSITORY object")

    def _parse_individual_types(self, type_combos: list[str]) -> list[str]:
        """Extract all individual types from a list of type combos.
        'fire-flying' -> ['fire', 'flying'], 'fire' -> ['fire']
        Deduplicates while preserving order.
        """
        seen = set()
        individual = []
        for combo in type_combos:
            for t in combo.split("-"):
                if t not in seen:
                    seen.add(t)
                    individual.append(t)
        return individual

    def _normalize_type_combo(self, type_combo: str) -> str:
        """Convert frontend format 'fire-flying' to index key format 'fire/flying'.
        Single types like 'fire' pass through unchanged.
        Handles canonical ordering by checking both orderings against the index.
        """
        if "-" not in type_combo:
            return type_combo

        parts = type_combo.split("-")
        forward = f"{parts[0]}/{parts[1]}"
        reverse = f"{parts[1]}/{parts[0]}"

        weakness_index = self.repository.get_opponent_weakness_type_index()
        if forward in weakness_index:
            return forward
        elif reverse in weakness_index:
            return reverse

        return forward

    def get_teams_type_strengths(self, individual_types: list[str]) -> dict[str, dict[str, frozenset[str]]]:
        """For each individual type, look up what defending types it hits effectively.
        Moves are single-typed, so strengths are always per individual type.

        Returns: {single_type: {"4x": frozenset(defending_types), ...}}
        """
        strengths_index = self.repository.get_my_team_strengths_type_index()
        results = {}

        for single_type in individual_types:
            if single_type in strengths_index:
                results[single_type] = strengths_index[single_type]
            else:
                logger.warning("Type not found in strengths index", single_type=single_type)

        return results

    def get_teams_type_weaknesses(self, type_combos: list[str]) -> dict[str, dict[str, frozenset[str]]]:
        """For each team slot, look up what attacking types hit that slot effectively.
        Preserves dual type combos since defense uses the full typing.

        Returns: {type_combo: {"4x": frozenset(attacking_types), ...}}
        """
        weakness_index = self.repository.get_opponent_weakness_type_index()
        results = {}

        for combo in type_combos:
            key = self._normalize_type_combo(combo)
            if key in weakness_index:
                results[key] = weakness_index[key]
            else:
                logger.warning("Type combo not found in weakness index", type_combo=combo, key=key)

        return results

    def _build_strengths_table(self, individual_types: list[str]) -> TypeCoverageTable:
        """Build table showing what each single type on your team hits effectively.
        Moves are single-typed, so each type is looked up individually.
        One row per defending type at 4x or 2x effectiveness.
        """
        strengths = self.get_teams_type_strengths(individual_types)
        rows = []

        for single_type, effectiveness in strengths.items():
            for enemy_type in sorted(effectiveness.get("4x", [])):
                rows.append(
                    TypeCoverageTableRow(
                        effectiveness="4x",
                        enemy_type=enemy_type,
                        friendly_type=single_type,
                    )
                )

            for enemy_type in sorted(effectiveness.get("2x", [])):
                rows.append(
                    TypeCoverageTableRow(
                        effectiveness="2x",
                        enemy_type=enemy_type,
                        friendly_type=single_type,
                    )
                )

        return TypeCoverageTable(rows=rows)

    def _build_weaknesses_table(self, type_combos: list[str]) -> TypeCoverageTable:
        """Build table showing what hits each team slot effectively (defensive).
        Preserves dual type combos since defense uses the full typing.
        One row per attacking type at 4x or 2x effectiveness.
        """
        weaknesses = self.get_teams_type_weaknesses(type_combos)
        rows = []

        for combo_key, effectiveness in weaknesses.items():
            friendly_type = combo_key.replace("/", " / ")

            for enemy_type in sorted(effectiveness.get("4x", [])):
                rows.append(
                    TypeCoverageTableRow(
                        effectiveness="4x",
                        enemy_type=enemy_type,
                        friendly_type=friendly_type,
                    )
                )

            for enemy_type in sorted(effectiveness.get("2x", [])):
                rows.append(
                    TypeCoverageTableRow(
                        effectiveness="2x",
                        enemy_type=enemy_type,
                        friendly_type=friendly_type,
                    )
                )

        return TypeCoverageTable(rows=rows)

    def build_response(self, type_combos: list[str]) -> CoverageAnalyzerResponse:
        logger.info("Building coverage response", slot_count=len(type_combos))

        # Validate all individual types via repository (raises InvalidPokemonTypeError)
        individual_types = self._parse_individual_types(type_combos)
        self.repository.validate_pokemon_types(*individual_types)

        response = CoverageAnalyzerResponse(
            team_strengths_table=self._build_strengths_table(individual_types),
            team_weaknesses_table=self._build_weaknesses_table(type_combos),
        )

        return response
