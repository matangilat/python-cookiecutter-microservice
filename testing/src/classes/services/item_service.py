"""Business logic service for items."""
from typing import List, Optional
from datetime import datetime

from src.classes.models.schemas import ItemCreate, ItemResponse
from src.classes.repositories.item_repository import ItemRepository


class ItemService:
    """Service layer for item business logic."""
    
    def __init__(self, repository: ItemRepository):
        """Initialize service with repository."""
        self.repository = repository
    
    async def list_items(self, skip: int = 0, limit: int = 100) -> List[ItemResponse]:
        """List items with pagination."""
        items = await self.repository.find_all(skip=skip, limit=limit)
        return [ItemResponse.from_orm(item) for item in items]
    
    async def get_item(self, item_id: str) -> Optional[ItemResponse]:
        """Get item by ID."""
        item = await self.repository.find_by_id(item_id)
        if item:
            return ItemResponse.from_orm(item)
        return None
    
    async def create_item(self, item_data: ItemCreate) -> ItemResponse:
        """Create a new item."""
        item = await self.repository.create(item_data.dict())
        return ItemResponse.from_orm(item)
    
    async def update_item(self, item_id: str, item_data: ItemCreate) -> Optional[ItemResponse]:
        """Update an existing item."""
        update_data = item_data.dict()
        update_data["updated_at"] = datetime.utcnow()
        
        item = await self.repository.update(item_id, update_data)
        if item:
            return ItemResponse.from_orm(item)
        return None
    
    async def delete_item(self, item_id: str) -> bool:
        """Delete an item."""
        return await self.repository.delete(item_id)
