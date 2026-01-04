
from pydantic import BaseModel, Field
# Pydantic Schemas for each type of table entry

# Move response
class MoveListing(BaseModel):
    pass

# Stats response
class StatsListing(BaseModel):
    pass

# Type response
class TypeListing(BaseModel):
    pass

# Type matchup response
class TypeMatchupListing(BaseModel):
    pass
