from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # DB URLS
    dev_database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/postgres-dev"
    unit_test_database_url: str = "sqlite+aiosqlite:///:memory:"  # in-memory SQLite for unit tests
    prod_database_url: str = ""

    # Litestar
    cors_origins: list[str] = ["*"]
    log_level: str = "INFO"

    # Env
    environment: str = "development"
    debug: bool = False

    # Data
    dataset: str = "pokerogue"
    backend_dir: Path = Path(__file__).parent.parent.parent
    data_dir: Path = backend_dir / "data"
    
    # Dynamic Pathing for multiple datasets
    @property
    def fixtures_dir(self) -> Path:
        return self.data_dir / "fixtures" / self.dataset
    
    # Fixture paths
    @property
    def tm_fixture_path(self) -> Path:
        return self.fixtures_dir / "tm.json"
        
    @property
    def pokemon_move_fixture_path(self) -> Path:
        return self.fixtures_dir / "pokemon_move.json"
    
    @property
    def pokemon_stats_fixture_path(self) -> Path:
        return self.fixtures_dir / "pokemon_stats.json"
    
    @property
    def pokemon_type_fixture_path(self) -> Path:
        return self.fixtures_dir / "pokemon_type.json"
    
    @property
    def pokemon_fixture_path(self) -> Path:
        return self.fixtures_dir / "pokemon.json"
    
    @property
    def stat_spreads_fixture_path(self) -> Path:
        return self.fixtures_dir / "stat_spreads.json"
    
    @property
    def type_matchups_fixture_path(self) -> Path:
        return self.fixtures_dir / "type_matchups.json"
    
    @property
    def db_url(self) -> str:
        """Returns appropriate DB based on environment"""
        if self.environment == "production":
            return self.prod_database_url
        else:
            return self.dev_database_url
        

# Settings generator and getter
@lru_cache
def get_settings() -> Settings:
    return Settings()



settings = get_settings()