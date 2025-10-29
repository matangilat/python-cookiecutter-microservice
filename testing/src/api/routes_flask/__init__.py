"""Flask route initialization."""
from .health_bp import health_bp
from .api_bp import api_bp

__all__ = ["health_bp", "api_bp"]
