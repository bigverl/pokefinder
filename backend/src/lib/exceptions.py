# ====================================
# Custom exceptions used throughout program
# ====================================


# =============
# Service layer
# =============

# Generic
class PokemonSearchError(Exception):
    pass

# Stat not found on list (invalid stat)
class InvalidPokemonStatError(PokemonSearchError):
    pass
    
# Pokemon type not found on list (invalid type)
class InvalidPokemonTypeError(PokemonSearchError):
    pass

# Search returns no results
class NoPokemonFoundError(PokemonSearchError):
    pass

# > 2 types provided
class TooManyTypesError(PokemonSearchError):
    pass

# Invalid pokemon move
class InvalidPokemonMoveError(PokemonSearchError):
    pass

# Invalid pokemon nmae
class InvalidPokemonNameError(PokemonSearchError):
    pass

# No search params
class NoSearchParamsError(PokemonSearchError):
    pass