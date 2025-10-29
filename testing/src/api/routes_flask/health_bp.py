"""Health check routes for Flask."""
from flask import Blueprint, jsonify, current_app
import asyncio
from functools import wraps

health_bp = Blueprint("health", __name__)


def async_route(f):
    """Decorator to run async functions in Flask routes."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(f(*args, **kwargs))
        finally:
            loop.close()
    return wrapper


@health_bp.route("/healthz")
def health_check():
    """Basic health check."""
    return jsonify({"status": "healthy"})


@health_bp.route("/ready")
@async_route
async def readiness_check():
    """Readiness check with dependency health."""
    checks = {
        "database": "healthy",
        "cache": "healthy",
    }
    
    # Check database
    if not await current_app.db_manager.health_check():
        checks["database"] = "unhealthy"
    
    # Check cache
    if not await current_app.cache_manager.health_check():
        checks["cache"] = "unhealthy"
    
    all_healthy = all(v == "healthy" for v in checks.values())
    
    return jsonify({
        "status": "ready" if all_healthy else "not_ready",
        "checks": checks
    }), 200 if all_healthy else 503
