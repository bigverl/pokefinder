from functools import lru_cache

import httpx
from pydantic_settings import BaseSettings, SettingsConfigDict

from frontend.modules.candidate_finder.schemas import CandidateFinderResponse
from frontend.modules.coverage_analyzer.schemas import CoverageAnalyzerResponse


class ApiConfig(BaseSettings):
    backend_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


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
        include_ultra_beasts: bool = False,
    ) -> CandidateFinderResponse:
        params = {
            "move": move,
            "desired_type": desired_type,
            "primary_stat": primary_stat,
            "secondary_stat": secondary_stat,
            "min_primary": min_primary,
            "min_secondary": min_secondary,
            "min_speed": min_speed,
            "include_mythical": include_mythical,
            "include_legendary": include_legendary,
            "include_ultra_beasts": include_ultra_beasts,
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = await self.client.get("/search_pokemon", params=params)

        # If status raised, send proper error message
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ValueError(e.response.text) from e

        return CandidateFinderResponse(**response.json())

    async def search_team_coverage(self, slots: list[str]) -> CoverageAnalyzerResponse:
        params = {}
        for i, slot in enumerate(slots, start=1):
            params[f"slot_{i}"] = slot

        response = await self.client.get("/team_coverage", params=params)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ValueError(e.response.text) from e

        return CoverageAnalyzerResponse(**response.json())

    async def close(self):
        await self.client.aclose()
