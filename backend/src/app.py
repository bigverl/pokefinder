import structlog
from litestar import Litestar
from litestar.di import Provide
from litestar.config.cors import CORSConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.plugins.structlog import StructlogPlugin
from advanced_alchemy.extensions.litestar import (
    SQLAlchemyPlugin,
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig
)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Custom Modules
from backend.src.modules.candidate_finder.deps import provide_candidate_finder
from backend.src.config.settings import settings

# Controllers
from backend.src.modules.candidate_finder.controllers import CandidateFinderController

logger = structlog.get_logger(__name__)

# CORS Origins
cors_config = CORSConfig(allow_origins=settings.cors_origins)

# Rate limiter
rate_limit_config = RateLimitConfig(
    rate_limit=("minute", 100),
    exclude=["/health", "/schema"]
)

# Database
engine = create_async_engine(settings.db_url)
alchemy_config = SQLAlchemyAsyncConfig(
    engine_instance=engine,
    session_config=AsyncSessionConfig(expire_on_commit=False)
)

# Startup hook to verify DB connection
async def check_db_connection(app: Litestar) -> None:
    """Verify database is reachable on startup."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection verified", db_url=settings.db_url.split("@")[-1])
    except Exception as e:
        logger.error(
            "Cannot connect to database. Is the container running?",
            db_url=settings.db_url.split("@")[-1],
            error=str(e)
        )
        raise RuntimeError(
            f"Cannot connect to database at {settings.db_url.split('@')[-1]}. "
            "Is the database container running?"
        ) from e

# App
app = Litestar(
    route_handlers=[CandidateFinderController],
    dependencies={
        "finder": Provide(provide_candidate_finder)},
    cors_config=cors_config,
    middleware=[rate_limit_config.middleware],
    plugins=[
        StructlogPlugin(),
        SQLAlchemyPlugin(config=alchemy_config)],
    on_startup=[check_db_connection]
)

