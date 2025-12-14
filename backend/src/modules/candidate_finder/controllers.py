
import json

from litestar import get, Controller, Request, Response, MediaType
from litestar.exceptions import NotFoundException, ClientException
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from backend.src.modules.candidate_finder.urls import (
    HEALTH,
    POKEMON,
    POKEMON_NAME,
    TYPE_MATCHUPS
)

from backend.src.lib.exceptions import (
    InvalidPokemonMoveError,
    InvalidPokemonTypeError,
    InvalidPokemonStatError,
    NoPokemonFoundError,
    TooManyTypesError,

)

from backend.src.modules.candidate_finder.schemas import (
    PokemonInfoResponse,
    PokemonTypeResponse,
    PokemonMoveResponse,
    PokemonStatsResponse,
    TypeMatchupResponse
)

from backend.src.modules.candidate_finder.deps import CandidateFinderService
from backend.src.config.settings import settings

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


class CandidateFinderController(Controller):
    path = ""  # Routes already have full paths from urls.py

    exception_handlers = {
        InvalidPokemonMoveError: invalid_pokemon_move_error_handler,
        InvalidPokemonStatError: invalid_pokemon_stat_error_handler,
        InvalidPokemonTypeError: invalid_pokemon_type_error_handler,        
        NoPokemonFoundError: no_pokemon_found_error_handler,
        TooManyTypesError: too_many_types_error_handler
    }

    @get(HEALTH)
    async def health_check(self) -> dict:
        return { "status": "healthy" }
        
    @get (POKEMON_NAME)
    async def pokemon_name(
        self, 
        finder: CandidateFinderService,
        name: str | None = None
        ) -> PokemonInfoResponse:

        if not name:
            raise ClientException(detail="Name required")
        
        results = finder.get_pokemon_by_name(name)

        if results:
            return PokemonInfoResponse(name = name, **results)
        else:
            raise NotFoundException(detail=f"pokemon {name!r} not found")
        
    @get(POKEMON)
    async def pokemon_list(
        self,
        finder: CandidateFinderService,
        move: str | None = None,
        types: str | None = None,
        primary_stat: str | None = None,
        secondary_stat: str | None = None,
        min_primary: int = 0,
        min_secondary: int | None = None,
        min_speed: int | None = None,
        include_mythical: bool = False,
        include_legendary: bool = False,
        include_ultra_beasts: bool = False
    ) -> PokemonMoveResponse | PokemonTypeResponse | PokemonStatsResponse:
            # Split types by hyphen to support dual types (e.g., "fire" or "fire-flying")
        if types:
            type_list = types.split('-')

        if move:
            results = finder.get_pokemon_by_move(
            move,
            include_legendary=include_legendary,
            include_mythical=include_mythical,
            include_ultra_beasts=include_ultra_beasts
            )
            return PokemonMoveResponse(move_name=move, pokemon_list=results)

        elif types:
            # Split types by hyphen to support dual types (e.g., "fire" or "fire-flying")
            type_list = types.split('-')

            results = finder.get_pokemon_by_type(
                *type_list,  # Now unpacks the list, not the string
                include_legendary=include_legendary,
                include_mythical=include_mythical,
                include_ultra_beasts=include_ultra_beasts
            )
        
            return PokemonTypeResponse(type_combo=types, pokemon_list=results)

        elif primary_stat and secondary_stat:
            results = finder.get_pokemon_by_stats(
                primary_stat,
                secondary_stat,
                min_primary=min_primary,
                min_secondary=min_secondary,
                min_speed=min_speed,
                include_mythical=include_mythical,
                include_legendary=include_legendary,
                include_ultra_beasts=include_ultra_beasts
                )
            return PokemonStatsResponse(root=results) #dict[str,dict]:
            
        else:
            # Return all or implement pagination
            raise ClientException(detail="Must specify type, move, or stats filter")
    
    @get(TYPE_MATCHUPS)
    async def type_matchups(
            self,
            finder: CandidateFinderService,
            types: str | None = None
            ) -> TypeMatchupResponse:
        
            if types:
                type_list = types.split('-')

                results = finder.get_type_effectiveness(*type_list)

                return TypeMatchupResponse(root=results)
            else:
                raise ClientException(detail="Must specify type(s)")