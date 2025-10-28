"""Base repository with common CRUD operations."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseRepository(ABC):
    """Abstract base repository."""
    
    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Any]:
        """Find all records."""
        pass
    
    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[Any]:
        """Find record by ID."""
        pass
    
    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> Any:
        """Create a new record."""
        pass
    
    @abstractmethod
    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Any]:
        """Update a record."""
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete a record."""
        pass
