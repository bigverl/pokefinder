import logging
from typing import Any

from litestar import (
    get, 
    Controller, 
    Request, 
    Response, 
    MediaType
)

from litestar.status_codes import (
    HTTP_400_BAD_REQUEST, 
    HTTP_404_NOT_FOUND
) 

from litestar.exceptions import NotFoundException, ClientException

from backend.src.modules.candidate_finder.urls import (
    HEALTH,
    SEARCH_POKEMON,
)

from backend.src.lib.exceptions import (
    InvalidPokemonMoveError,
    InvalidPokemonTypeError,
    InvalidPokemonStatError,
    NoPokemonFoundError,
    TooManyTypesError,
    NoSearchParamsError
)

from backend.src.modules.candidate_finder.schemas import CandidateFinderResponse

from backend.src.modules.candidate_finder.deps import CandidateFinderService

logger = logging.getLogger(__name__)

# Error handlers
def invalid_pokemon_type_error_handler(_: Request, exc: InvalidPokemonTypeError) -> Response:
    return Response(
        media_type=MediaType.TEXT,
        content=str(exc),
        status_code=HTTP_400_BAD_REQUEST,
    )

def no_pokemon_found_error_handler(_: Request, exc: NoPokemonFoundError) -> Response:
    return Response(
        media_type=MediaType.TEXT,
        content=str(exc),
        status_code=HTTP_404_NOT_FOUND,
    )

def too_many_types_error_handler(_: Request, exc: TooManyTypesError) -> Response:
    return Response(
        media_type=MediaType.TEXT,
        content=str(exc),
        status_code=HTTP_400_BAD_REQUEST,
    )

def invalid_pokemon_move_error_handler(_: Request, exc: InvalidPokemonMoveError) -> Response:
    return Response(
        media_type=MediaType.TEXT,
        content=str(exc),
        status_code=HTTP_400_BAD_REQUEST,
    )

def invalid_pokemon_stat_error_handler(_: Request, exc: InvalidPokemonStatError) -> Response:
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

class CandidateFinderController(Controller):
    path = ""  # Routes already have full paths from urls.py

    exception_handlers = {
        InvalidPokemonMoveError: invalid_pokemon_move_error_handler,
        InvalidPokemonStatError: invalid_pokemon_stat_error_handler,
        InvalidPokemonTypeError: invalid_pokemon_type_error_handler,        
        NoPokemonFoundError: no_pokemon_found_error_handler,
        TooManyTypesError: too_many_types_error_handler,
        NoSearchParamsError: no_search_params_error_handler
    }

    @get(HEALTH)
    async def health_check(self) -> dict:
        return { "status": "healthy" }
    
    @get(SEARCH_POKEMON)
    async def search_pokemon(
        self,
        finder: CandidateFinderService,
        move: str | None = None,
        desired_type: str | None = None,
        primary_stat: str | None = None,
        secondary_stat: str | None = None,
        min_primary: str | None = None,
        min_secondary: str | None = None,
        min_speed: str | None = None,
        include_mythical: bool = False,
        include_legendary: bool = False,
        include_ultra_beasts: bool = False
    ) -> CandidateFinderResponse:

        # Case 1: No params
        if not any([move, desired_type, primary_stat, secondary_stat]):
            raise NoSearchParamsError("Must provide at least one search parameter")
        
        # Get results
        response: frozenset[str] = finder.search_pokemon(
            move=move,
            desired_type=desired_type,
            primary_stat=primary_stat,
            secondary_stat=secondary_stat,
            min_primary=int(min_primary) if min_primary else 0,
            min_secondary=int(min_secondary) if min_secondary else None,
            min_speed=int(min_speed) if min_speed else None,
            include_legendary=include_legendary,
            include_mythical=include_mythical,
            include_ultra_beasts=include_ultra_beasts
        )

        # Case 2: No pokemon found
        if not response:
            raise NotFoundException(
                detail="No pokemon found. Try loosening filters."
                )

        # Populate tables
        params = {"move": move}
        results = finder.build_response(response, params)

        # Return tables
        return results