"""Item repository implementation."""

from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

from sqlalchemy import select
from src.classes.repositories.base_repository import BaseRepository
from src.classes.models.entities import Item


class ItemRepository(BaseRepository):
    """SQLAlchemy repository for items."""
    
    def __init__(self, db_manager):
        """Initialize with database manager."""
        self.db_manager = db_manager
    
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """Find all items."""
        connection = await self.db_manager.get_connection()
        
        query = select(Item).offset(skip).limit(limit)
        result = await connection.execute(query)
        return result.scalars().all()
    
    async def find_by_id(self, id: str) -> Optional[Item]:
        """Find item by ID."""
        connection = await self.db_manager.get_connection()
        
        query = select(Item).where(Item.id == id)
        result = await connection.execute(query)
        return result.scalar_one_or_none()
    
    async def create(self, data: Dict[str, Any]) -> Item:
        """Create a new item."""
        connection = await self.db_manager.get_connection()
        
        item = Item(id=str(uuid.uuid4()), **data)
        connection.add(item)
        await connection.commit()
        await connection.refresh(item)
        
        return item
    
    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Item]:
        """Update an item."""
        item = await self.find_by_id(id)
        if not item:
            return None
        
        connection = await self.db_manager.get_connection()
        
        for key, value in data.items():
            setattr(item, key, value)
        
        await connection.commit()
        await connection.refresh(item)
        
        return item
    
    async def delete(self, id: str) -> bool:
        """Delete an item."""
        item = await self.find_by_id(id)
        if not item:
            return False
        
        connection = await self.db_manager.get_connection()
        await connection.delete(item)
        await connection.commit()
        
        return True

