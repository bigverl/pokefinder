from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = "postgresql+asyncpg://localhost:5432/pokepicker"
    integration_test_database_url: str = "postgresql+asyncpg://localhost:5432/pokepicker_test"
    unit_test_database_url: str = "sqlite+aiosqlite:///:memory:"

    # API
    cors_origins: list[str] = ["*"]
    log_level: str = "INFO"

    # App
    dataset: str = "pokerogue"
    environment: str = "development"
    debug: bool = False

    @property
    def db_url(self) -> str:
        """Returns appropriate DB based on test type"""
        test_mode = os.getenv("TEST_MODE")
        if test_mode == "unit":
            return self.unit_test_database_url
        elif test_mode == "integration":
            return self.integration_test_database_url
        return self.database_url

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()