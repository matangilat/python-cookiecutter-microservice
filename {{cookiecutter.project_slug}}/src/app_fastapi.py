"""FastAPI application entry point."""
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from src.api.routes import health, api_v1
from src.infrastructure.database import DatabaseManager
from src.infrastructure.cache import CacheManager
from src.infrastructure.metrics import MetricsCollector
from src.config import Settings, InfrastructureConfig
from src.utils.logging import setup_logging


# Initialize configuration
settings = Settings()
infra_config = InfrastructureConfig()
setup_logging(settings.LOG_LEVEL)

# Initialize infrastructure managers
db_manager = DatabaseManager(settings, infra_config)
cache_manager = CacheManager(settings, infra_config)
metrics = MetricsCollector()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application lifespan."""
    # Startup
    await db_manager.initialize()
    await cache_manager.initialize()
    
    # Store managers in app state for access in routes
    app.state.db_manager = db_manager
    app.state.cache_manager = cache_manager
    app.state.metrics = metrics
    
    yield
    
    # Shutdown
    await cache_manager.close()
    await db_manager.close()


app = FastAPI(
    title="{{ cookiecutter.project_name }}",
    description="{{ cookiecutter.project_description }}",
    version="1.0.0",
    lifespan=lifespan,
)


# Middleware for metrics
@app.middleware("http")
async def metrics_middleware(request, call_next):
    """Track HTTP metrics."""
    response = await call_next(request)
    metrics.track_request(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code,
    )
    return response


# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(api_v1.router, prefix="/api/v1", tags=["API"])


@app.get("/metrics", response_class=PlainTextResponse)
async def metrics_endpoint():
    """Prometheus metrics endpoint."""
    return generate_latest()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.app_fastapi:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
