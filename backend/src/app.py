from pathlib import Path

import structlog
from litestar import Litestar, Request
from litestar.config.cors import CORSConfig
from litestar.di import Provide
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.plugins.structlog import StructlogPlugin
from litestar.static_files import StaticFilesConfig

from backend.src.config.settings import settings
from backend.src.lib.repository import JSONRepository

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


# Startup hook — load JSON fixtures once and store services as singletons
def startup(app: Litestar) -> None:
    repo = JSONRepository()
    app.state.candidate_finder_service = CandidateFinderService(repository=repo)
    app.state.coverage_analyzer_service = CoverageAnalyzerService(repository=repo)
    logger.info("CandidateFinderService initialized (singleton)")
    logger.info("CoverageAnalyzerService initialized (singleton)")


def provide_candidate_finder(request: Request) -> CandidateFinderService:
    return request.app.state.candidate_finder_service


def provide_coverage_analyzer(request: Request) -> CoverageAnalyzerService:
    return request.app.state.coverage_analyzer_service


_dist = Path("frontend/dist")

# App
app = Litestar(
    route_handlers=[CandidateFinderController, CoverageAnalyzerController],
    static_files_config=[
        StaticFilesConfig(directories=[_dist], path="/", html_mode=True),
    ] if _dist.exists() else [],
    dependencies={
        "finder": Provide(provide_candidate_finder, sync_to_thread=False),
        "coverage_analyzer": Provide(provide_coverage_analyzer, sync_to_thread=False),
    },
    cors_config=cors_config,
    middleware=[rate_limit_config.middleware],
    plugins=[StructlogPlugin()],
    on_startup=[startup],
)
