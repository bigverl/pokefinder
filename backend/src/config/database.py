from functools import lru_cache
from advanced_alchemy.extensions.litestar import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig
)

from backend.src.config.settings import settings

@lru_cache(maxsize=1)
def create_db_config() -> SQLAlchemyAsyncConfig:
    return SQLAlchemyAsyncConfig(
        connection_string=settings.db_url,
        session_config = AsyncSessionConfig(expire_on_commit=False),
        before_send_handler="autocommit"
    )

