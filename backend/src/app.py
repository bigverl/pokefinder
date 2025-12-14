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

# Custom Modules
from backend.src.modules.candidate_finder.deps import provide_candidate_finder
from backend.src.config.settings import settings

# Controllers
from backend.src.modules.candidate_finder.controllers import CandidateFinderController

# Providers


# CORS Origins
cors_config = CORSConfig(allow_origins=settings.cors_origins)

# Rate limiter
rate_limit_config = RateLimitConfig(
    rate_limit=("minute", 100),
    exclude=["/health", "/schema"]
)

# Database
alchemy_config = SQLAlchemyAsyncConfig(
    engine_instance=create_async_engine(settings.db_url),
    session_config=AsyncSessionConfig(expire_on_commit=False)
)

# App
app = Litestar(
    route_handlers=[CandidateFinderController],
    dependencies={
        "finder": Provide(provide_candidate_finder)},
    cors_config=cors_config,
    middleware=[rate_limit_config.middleware],
    plugins=[
        StructlogPlugin(),
        SQLAlchemyPlugin(config=alchemy_config)]
)

