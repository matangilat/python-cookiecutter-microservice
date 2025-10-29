"""Dependency injection for FastAPI and Flask."""
from flask import current_app
from src.classes.repositories.item_repository import ItemRepository
from src.classes.services.item_service import ItemService


# Flask dependencies
async def get_item_repository_flask() -> ItemRepository:
    """Get item repository instance for Flask."""
    return ItemRepository(current_app.db_manager)


async def get_item_service_flask() -> ItemService:
    """Get item service instance for Flask."""
    repository = await get_item_repository_flask()
    return ItemService(repository)
