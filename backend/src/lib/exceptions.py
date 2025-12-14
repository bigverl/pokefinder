# ====================================
# Custom exceptions used throughout program
# ====================================


# =============
# Service layer
# =============
class PokemonSearchError(Exception):
    """Base exception for Pokemon search errors."""
    pass

class InvalidPokemonTypeError(PokemonSearchError):
    """Raised when an invalid Pokemon type is provided."""
    pass

class NoPokemonFoundError(PokemonSearchError):
    """Raised when search returns no results."""
    pass

class TooManyTypesError(PokemonSearchError):
    """Raised when more than 2 types are provided."""
    pass


class InvalidPokemonMoveError(PokemonSearchError):
    """Raised when invalid pokemon move provided"""
    pass

class InvalidPokemonNameError(PokemonSearchError):
    """Raised when invalid pokemon name provided"""
    pass

class InvalidPokemonStatError(PokemonSearchError):
    """Raised when invalid pokemon stat provided"""
    pass