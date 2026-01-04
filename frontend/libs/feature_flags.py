from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class FeatureFlags(BaseSettings):
  pokedex: bool = False
  coverage_analyzer: bool = False

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
    env_prefix="FEATURE_"
    )

@lru_cache
def get_features():
  return FeatureFlags()

FEATURE_FLAGS = get_features()