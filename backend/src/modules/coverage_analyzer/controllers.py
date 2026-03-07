from litestar import Controller, MediaType, Request, Response, get
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
)

from backend.src.lib.exceptions import InvalidPokemonTypeError, NoSearchParamsError
from backend.src.modules.coverage_analyzer.schemas import CoverageAnalyzerResponse
from backend.src.modules.coverage_analyzer.services import CoverageAnalyzerService

TEAM_COVERAGE = "/team_coverage"


# Error handlers
def invalid_pokemon_type_error_handler(_: Request, exc: InvalidPokemonTypeError) -> Response:
    return Response(
        media_type=MediaType.TEXT,
        content=str(exc),
        status_code=HTTP_400_BAD_REQUEST,
    )


def no_search_params_error_handler(_: Request, exc: NoSearchParamsError) -> Response:
    return Response(
        media_type=MediaType.TEXT,
        content=str(exc),
        status_code=HTTP_400_BAD_REQUEST,
    )


class CoverageAnalyzerController(Controller):
    path = ""

    exception_handlers = {
        InvalidPokemonTypeError: invalid_pokemon_type_error_handler,
        NoSearchParamsError: no_search_params_error_handler,
    }

    @get(TEAM_COVERAGE)
    async def team_coverage(
        self,
        coverage_analyzer: CoverageAnalyzerService,
        slot_1: str | None = None,
        slot_2: str | None = None,
        slot_3: str | None = None,
        slot_4: str | None = None,
        slot_5: str | None = None,
        slot_6: str | None = None,
    ) -> CoverageAnalyzerResponse:

        slots = [s for s in [slot_1, slot_2, slot_3, slot_4, slot_5, slot_6] if s]

        if not slots:
            raise NoSearchParamsError("Must provide at least one team slot")

        return coverage_analyzer.build_response(slots)
