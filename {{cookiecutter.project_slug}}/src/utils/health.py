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
            {% if cookiecutter.database_type == 'postgresql' %}
            # PostgreSQL check
            await db_manager.execute_query("SELECT 1")
            {% elif cookiecutter.database_type == 'mysql' %}
            # MySQL check
            await db_manager.execute_query("SELECT 1")
            {% elif cookiecutter.database_type == 'mongodb' %}
            # MongoDB check
            await db_manager.db.command('ping')
            {% endif %}
            return {
                "status": "healthy",
                "type": "{{ cookiecutter.database_type }}",
                "response_time_ms": round((time.time() - start) * 1000, 2)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "type": "{{ cookiecutter.database_type }}",
                "error": str(e),
                "response_time_ms": round((time.time() - start) * 1000, 2)
            }
    
    async def check_cache(self, cache_manager) -> Dict[str, Any]:
        """Check cache connection."""
        start = time.time()
        try:
            {% if cookiecutter.cache_type == 'redis' %}
            # Redis check
            await cache_manager.client.ping()
            {% elif cookiecutter.cache_type == 'memcached' %}
            # Memcached check
            await cache_manager.client.set('health_check', '1', expire=1)
            await cache_manager.client.get('health_check')
            {% endif %}
            return {
                "status": "healthy",
                "type": "{{ cookiecutter.cache_type }}",
                "response_time_ms": round((time.time() - start) * 1000, 2)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "type": "{{ cookiecutter.cache_type }}",
                "error": str(e),
                "response_time_ms": round((time.time() - start) * 1000, 2)
            }
    
    async def check_queue(self) -> Dict[str, Any]:
        """Check message queue connection."""
        start = time.time()
        try:
            {% if cookiecutter.queue_type == 'kafka' %}
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
            {% elif cookiecutter.queue_type == 'rabbitmq' %}
            # RabbitMQ check
            import aio_pika
            
            connection = await aio_pika.connect_robust(
                f"amqp://{self.settings.QUEUE_HOST}"
            )
            await connection.close()
            
            return {
                "status": "healthy",
                "type": "rabbitmq",
                "response_time_ms": round((time.time() - start) * 1000, 2)
            }
            {% elif cookiecutter.queue_type == 'sqs' %}
            # SQS check
            import boto3
            
            sqs = boto3.client('sqs', region_name=self.settings.AWS_REGION)
            response = sqs.list_queues()
            
            return {
                "status": "healthy",
                "type": "sqs",
                "queues_count": len(response.get('QueueUrls', [])),
                "response_time_ms": round((time.time() - start) * 1000, 2)
            }
            {% else %}
            return {
                "status": "not_configured",
                "type": "none"
            }
            {% endif %}
        except Exception as e:
            return {
                "status": "unhealthy",
                "type": "{{ cookiecutter.queue_type }}",
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
        {% if cookiecutter.database_type != 'none' %}
        if db_manager:
            db_health = await self.check_database(db_manager)
            checks["checks"]["database"] = db_health
            if db_health["status"] != "healthy":
                checks["status"] = "degraded"
        {% endif %}
        
        # Check cache
        {% if cookiecutter.cache_type != 'none' %}
        if cache_manager:
            cache_health = await self.check_cache(cache_manager)
            checks["checks"]["cache"] = cache_health
            if cache_health["status"] != "healthy":
                checks["status"] = "degraded"
        {% endif %}
        
        # Check queue
        {% if cookiecutter.queue_type != 'none' %}
        queue_health = await self.check_queue()
        checks["checks"]["queue"] = queue_health
        if queue_health["status"] != "healthy":
            checks["status"] = "degraded"
        {% endif %}
        
        checks["total_response_time_ms"] = round((time.time() - start_time) * 1000, 2)
        
        return checks
