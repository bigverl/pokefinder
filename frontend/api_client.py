from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import httpx
from backend.src.modules.candidate_finder.schemas import CandidateFinderResponse

class ApiConfig(BaseSettings):
    backend_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="API_"
    )

@lru_cache
def get_api_config():
    return ApiConfig()

API_CONFIG = get_api_config()

class BackendClient:
    def __init__(self, base_url: str = API_CONFIG.backend_url):
        self.client = httpx.AsyncClient(base_url=base_url, timeout=3.0)


    async def search_pokemon(
        self,
        move: str | None = None,
        desired_type: str | None = None,
        primary_stat: str | None = None,
        secondary_stat: str | None = None,
        min_primary: int = 0,
        min_secondary: int | None = None,
        min_speed: int | None = None,
        include_mythical: bool = False,
        include_legendary: bool = False,
        include_ultra_beasts: bool = False
    ) -> CandidateFinderResponse:
        params = {
            "move": move,
            "desired_type": desired_type,
            "primary_stat": primary_stat,
            "secondary_stat":  secondary_stat,
            "min_primary": min_primary,
            "min_secondary": min_secondary,
            "min_speed": min_speed,
            "include_mythical": include_mythical,
            "include_legendary": include_legendary,
            "include_ultra_beasts": include_ultra_beasts,
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = await self.client.get("/search_pokemon", params=params)
        response.raise_for_status()

        return CandidateFinderResponse(**response.json())

    async def close(self):
        await self.client.aclose()
