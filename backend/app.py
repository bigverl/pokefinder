from litestar import Litestar
from litestar.di import Provide
from litestar.config.cors import CORSConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.plugins.structlog import StructlogPlugin

from backend.candidate_finder.controllers import CandidateFinderController
from backend.candidate_finder.deps import provide_sqlite_candidate_finder
from config import ALLOWED_CORS_ORIGINS

cors_config = CORSConfig(allow_origins=ALLOWED_CORS_ORIGINS)

rate_limit_config = RateLimitConfig(
    rate_limit=("minute", 100),
    exclude=["/health", "/schema"]
)

app = Litestar(
    route_handlers=[CandidateFinderController],
    dependencies={"finder": Provide(provide_sqlite_candidate_finder)},
    cors_config=cors_config,
    middleware=[rate_limit_config.middleware],
    plugins=[StructlogPlugin()]
)

