import structlog
from advanced_alchemy.extensions.litestar import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar import Litestar, Request
from litestar.config.cors import CORSConfig
from litestar.di import Provide
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.plugins.structlog import StructlogPlugin
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from backend.src.config.settings import settings

# Custom Modules
from backend.src.lib.repository import SQLAlchemyRepository

# Controllers
from backend.src.modules.candidate_finder.controllers import CandidateFinderController
from backend.src.modules.candidate_finder.services import CandidateFinderService
from backend.src.modules.coverage_analyzer.controllers import CoverageAnalyzerController
from backend.src.modules.coverage_analyzer.services import CoverageAnalyzerService

logger = structlog.get_logger(__name__)

# CORS Origins
cors_config = CORSConfig(allow_origins=settings.cors_origins)

# Rate limiter
rate_limit_config = RateLimitConfig(rate_limit=("minute", 100), exclude=["/health", "/schema"])

# Database
engine = create_async_engine(settings.database_url)
alchemy_config = SQLAlchemyAsyncConfig(
    engine_instance=engine, session_config=AsyncSessionConfig(expire_on_commit=False)
)


# Startup hook to verify DB connection and init repository
async def startup(app: Litestar) -> None:
    # Check DB connection
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection verified", database_url=settings.database_url.split("@")[-1])
    except Exception as e:
        logger.error(
            "Cannot connect to database. Is the container running?",
            database_url=settings.database_url.split("@")[-1],
            error=str(e),
        )
        raise RuntimeError(
            f"Cannot connect to database at {settings.database_url.split('@')[-1]}. Is the database container running?"
        ) from e

    # Initialize singleton repository (load indexes once)
    async with AsyncSession(engine) as session:
        repo = await SQLAlchemyRepository.create(session=session)
        app.state.candidate_finder_service = CandidateFinderService(repository=repo)
        app.state.coverage_analyzer_service = CoverageAnalyzerService(repository=repo)
        logger.info("CandidateFinderService initialized (singleton)")
        logger.info("CoverageAnalyzerService initialized (singleton)")


def provide_candidate_finder(request: Request) -> CandidateFinderService:
    return request.app.state.candidate_finder_service


def provide_coverage_analyzer(request: Request) -> CoverageAnalyzerService:
    return request.app.state.coverage_analyzer_service


# App
app = Litestar(
    route_handlers=[CandidateFinderController, CoverageAnalyzerController],
    dependencies={
        "finder": Provide(provide_candidate_finder, sync_to_thread=False),
        "coverage_analyzer": Provide(provide_coverage_analyzer, sync_to_thread=False),
    },
    cors_config=cors_config,
    middleware=[rate_limit_config.middleware],
    plugins=[StructlogPlugin(), SQLAlchemyPlugin(config=alchemy_config)],
    on_startup=[startup],
)
