from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import httpx
from typing import Any

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
        self.client = httpx.Client(base_url=base_url, timeout=10.0)

    # def get_pokemon_by_move(
    #     self,
    #     move: str,
    #     include_legendary: bool = False,
    #     include_mythical: bool = False,
    #     include_ultra_beasts: bool = False
    # ) -> dict[str, Any]:
    #     response = self.client.get(
    #         "/pokemon",
    #         params={
    #             "move": move,
    #             "include_legendary": include_legendary,
    #             "include_mythical": include_mythical,
    #             "include_ultra_beasts": include_ultra_beasts
    #         }
    #     )
    #     response.raise_for_status()
    #     return response.json()

    # def get_pokemon_by_type(
    #     self,
    #     types: str,
    #     include_legendary: bool = False,
    #     include_mythical: bool = False,
    #     include_ultra_beasts: bool = False
    # ) -> dict[str, Any]:
    #     response = self.client.get(
    #         "/pokemon",
    #         params={
    #             "types": types,
    #             "include_legendary": include_legendary,
    #             "include_mythical": include_mythical,
    #             "include_ultra_beasts": include_ultra_beasts
    #         }
    #     )
    #     response.raise_for_status()
    #     return response.json()

    # def get_pokemon_by_stats(
    #     self,
    #     primary_stat: str,
    #     secondary_stat: str,
    #     min_primary: int = 0,
    #     min_secondary: int | None = None,
    #     min_speed: int | None = None,
    #     include_legendary: bool = False,
    #     include_mythical: bool = False,
    #     include_ultra_beasts: bool = False
    # ) -> dict[str, Any]:
    #     params = {
    #         "primary_stat": primary_stat,
    #         "secondary_stat": secondary_stat,
    #         "min_primary": min_primary,
    #         "include_legendary": include_legendary,
    #         "include_mythical": include_mythical,
    #         "include_ultra_beasts": include_ultra_beasts
    #     }
    #     if min_secondary is not None:
    #         params["min_secondary"] = min_secondary
    #     if min_speed is not None:
    #         params["min_speed"] = min_speed

    #     response = self.client.get("/pokemon", params=params)
    #     response.raise_for_status()
    #     return response.json()

    def get_type_matchups(self, types: str) -> dict[str, Any]:
        response = self.client.get("/type-matchups", params={"types": types})
        response.raise_for_status()
        return response.json()

    def close(self):
        self.client.close()
