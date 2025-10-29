"""Configuration management."""
from typing import Optional, Dict, Any
from pathlib import Path
import yaml
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Application
    APP_NAME: str = "testing"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    
    # Database
    DB_TYPE: str = "postgresql"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "testing"
    DB_USER: str = "admin"
    DB_PASSWORD: str = "changeme"
    
    # Cache
    CACHE_TYPE: str = "redis"
    CACHE_HOST: str = "localhost"
    CACHE_PORT: int = 6379
    CACHE_PASSWORD: Optional[str] = None
    
    # Queue
    QUEUE_TYPE: str = "kafka"
    QUEUE_HOST: str = "localhost"
    QUEUE_PORT: int = 9092
    QUEUE_USER: Optional[str] = None
    QUEUE_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


class InfrastructureConfig:
    """Infrastructure configuration from YAML."""
    
    def __init__(self, config_path: str = "config/infrastructure.yaml"):
        """Initialize from config file."""
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                self._config = yaml.safe_load(f) or {}
    
    @property
    def database(self) -> Optional[Dict[str, Any]]:
        """Get database configuration."""
        return self._config.get("database")
    
    @property
    def cache(self) -> Optional[Dict[str, Any]]:
        """Get cache configuration."""
        return self._config.get("cache")
    
    @property
    def queue(self) -> Optional[Dict[str, Any]]:
        """Get queue configuration."""
        return self._config.get("queue")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
