"""Metrics collector."""
{% if cookiecutter.enable_metrics == 'yes' %}
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Prometheus metrics collector."""
    
    def __init__(self):
        """Initialize metrics collector."""
        # Initialize Prometheus metrics here
        pass
    
    def track_request(self, method: str, endpoint: str, status_code: int) -> None:
        """Track HTTP request metrics."""
        pass
    
    def track_business_metric(self, metric_name: str, value: float) -> None:
        """Track business metrics."""
        pass
    
    def track_database_query(self, query_type: str, duration: float) -> None:
        """Track database query metrics."""
        pass
    
    def track_cache_operation(self, operation: str, hit: bool) -> None:
        """Track cache operation metrics."""
        pass
{% else %}
class MetricsCollector:
    """Dummy metrics collector when metrics are disabled."""
    
    def __init__(self):
        pass
    
    def track_request(self, method: str, endpoint: str, status_code: int) -> None:
        pass
    
    def track_business_metric(self, metric_name: str, value: float) -> None:
        pass
    
    def track_database_query(self, query_type: str, duration: float) -> None:
        pass
    
    def track_cache_operation(self, operation: str, hit: bool) -> None:
        pass
{% endif %}
