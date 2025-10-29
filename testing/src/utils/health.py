"""Health check utilities for infrastructure dependencies."""
import time
from typing import Dict, Any
from src.config import Settings, InfrastructureConfig


class HealthChecker:
    """Check health of all infrastructure dependencies."""
    
    def __init__(self, settings: Settings, infra_config: InfrastructureConfig):
        self.settings = settings
        self.infra_config = infra_config
    
    async def check_database(self, db_manager) -> Dict[str, Any]:
        """Check database connection."""
        start = time.time()
        try:
            
            # PostgreSQL check
            await db_manager.execute_query("SELECT 1")
            
            return {
                "status": "healthy",
                "type": "postgresql",
                "response_time_ms": round((time.time() - start) * 1000, 2)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "type": "postgresql",
                "error": str(e),
                "response_time_ms": round((time.time() - start) * 1000, 2)
            }
    
    async def check_cache(self, cache_manager) -> Dict[str, Any]:
        """Check cache connection."""
        start = time.time()
        try:
            
            # Redis check
            await cache_manager.client.ping()
            
            return {
                "status": "healthy",
                "type": "redis",
                "response_time_ms": round((time.time() - start) * 1000, 2)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "type": "redis",
                "error": str(e),
                "response_time_ms": round((time.time() - start) * 1000, 2)
            }
    
    async def check_queue(self) -> Dict[str, Any]:
        """Check message queue connection."""
        start = time.time()
        try:
            
            # Kafka check
            from kafka import KafkaAdminClient
            from kafka.errors import KafkaError
            
            admin_client = KafkaAdminClient(
                bootstrap_servers=self.settings.QUEUE_HOST,
                client_id='health_check'
            )
            # List topics to verify connection
            topics = admin_client.list_topics()
            admin_client.close()
            
            return {
                "status": "healthy",
                "type": "kafka",
                "topics_count": len(topics),
                "response_time_ms": round((time.time() - start) * 1000, 2)
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "type": "kafka",
                "error": str(e),
                "response_time_ms": round((time.time() - start) * 1000, 2)
            }
    
    async def check_all(self, db_manager=None, cache_manager=None) -> Dict[str, Any]:
        """Run all health checks."""
        start_time = time.time()
        
        checks = {
            "status": "healthy",
            "timestamp": time.time(),
            "checks": {}
        }
        
        # Check database
        
        if db_manager:
            db_health = await self.check_database(db_manager)
            checks["checks"]["database"] = db_health
            if db_health["status"] != "healthy":
                checks["status"] = "degraded"
        
        
        # Check cache
        
        if cache_manager:
            cache_health = await self.check_cache(cache_manager)
            checks["checks"]["cache"] = cache_health
            if cache_health["status"] != "healthy":
                checks["status"] = "degraded"
        
        
        # Check queue
        
        queue_health = await self.check_queue()
        checks["checks"]["queue"] = queue_health
        if queue_health["status"] != "healthy":
            checks["status"] = "degraded"
        
        
        checks["total_response_time_ms"] = round((time.time() - start_time) * 1000, 2)
        
        return checks
