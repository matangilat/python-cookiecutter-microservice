"""Flask application entry point."""
import asyncio
import atexit
from functools import wraps

from flask import Flask, jsonify, Response
{% if cookiecutter.enable_metrics == 'yes' -%}
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
{% endif -%}

from src.api.routes_flask import health_bp, api_bp
from src.utils.database import DatabaseManager
from src.utils.cache import CacheManager
{% if cookiecutter.enable_metrics == 'yes' -%}
from src.utils.metrics import MetricsCollector
{% endif -%}
from src.config import Settings, InfrastructureConfig
from src.utils.logging import setup_logging


# Initialize configuration
settings = Settings()
infra_config = InfrastructureConfig()
setup_logging(settings.LOG_LEVEL)

# Initialize infrastructure managers
db_manager = DatabaseManager(settings, infra_config)
cache_manager = CacheManager(settings, infra_config)
{% if cookiecutter.enable_metrics == 'yes' -%}
metrics = MetricsCollector()
{% endif -%}


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


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(settings)
    
    # Store managers in app context
    app.db_manager = db_manager
    app.cache_manager = cache_manager
{% if cookiecutter.enable_metrics == 'yes' -%}
    app.metrics = metrics
{% endif -%}
    
    # Initialize infrastructure on startup
    @app.before_first_request
    @async_route
    async def startup():
        await db_manager.initialize()
        await cache_manager.initialize()
    
    # Cleanup on shutdown
    def shutdown():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(cache_manager.close())
            loop.run_until_complete(db_manager.close())
        finally:
            loop.close()
    
    atexit.register(shutdown)
    
{% if cookiecutter.enable_metrics == 'yes' -%}
    # Middleware for metrics
    @app.before_request
    def before_request():
        from flask import request
        request._start_time = asyncio.get_event_loop().time()
    
    @app.after_request
    def after_request(response):
        from flask import request
        metrics.track_request(
            method=request.method,
            endpoint=request.endpoint or "unknown",
            status_code=response.status_code,
        )
        return response
    
{% endif -%}
    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    
{% if cookiecutter.enable_metrics == 'yes' -%}
    # Metrics endpoint
    @app.route("/metrics")
    def metrics_endpoint():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    
{% endif -%}
    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
    )
