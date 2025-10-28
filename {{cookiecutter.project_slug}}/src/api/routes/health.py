"""Health check routes for FastAPI."""
from fastapi import APIRouter, Response, status, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/healthz")
async def health_check():
    """Basic health check."""
    return JSONResponse(
        content={"status": "healthy"},
        status_code=status.HTTP_200_OK
    )


@router.get("/ready")
async def readiness_check(request: Request):
    """Readiness check with dependency health."""
    checks = {
        "database": "healthy",
        "cache": "healthy",
    }
    
    # Get managers from app state
    db_manager = getattr(request.app.state, 'db_manager', None)
    cache_manager = getattr(request.app.state, 'cache_manager', None)
    
    # Check database
    if db_manager and not await db_manager.health_check():
        checks["database"] = "unhealthy"
    
    # Check cache
    if cache_manager and not await cache_manager.health_check():
        checks["cache"] = "unhealthy"
    
    all_healthy = all(v == "healthy" for v in checks.values())
    
    return JSONResponse(
        content={
            "status": "ready" if all_healthy else "not_ready",
            "checks": checks
        },
        status_code=status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    )
