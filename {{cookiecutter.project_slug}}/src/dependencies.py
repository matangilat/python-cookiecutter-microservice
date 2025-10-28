"""Dependency injection for FastAPI and Flask."""
{% if cookiecutter.web_framework == 'flask' -%}
from flask import current_app
{% endif -%}
{% if cookiecutter.web_framework == 'fastapi' -%}
from fastapi import Depends, Request
{% endif -%}

from src.repositories.item_repository import ItemRepository
from src.services.item_service import ItemService


{% if cookiecutter.web_framework == 'fastapi' -%}
# FastAPI dependencies
async def get_item_repository(request: Request) -> ItemRepository:
    """Get item repository instance."""
    db_manager = getattr(request.app.state, 'db_manager', None)
    return ItemRepository(db_manager)


async def get_item_service(
    repository: ItemRepository = Depends(get_item_repository)
) -> ItemService:
    """Get item service instance."""
    return ItemService(repository)
{% endif -%}

{% if cookiecutter.web_framework == 'flask' -%}
# Flask dependencies
async def get_item_repository_flask() -> ItemRepository:
    """Get item repository instance for Flask."""
    return ItemRepository(current_app.db_manager)


async def get_item_service_flask() -> ItemService:
    """Get item service instance for Flask."""
    repository = await get_item_repository_flask()
    return ItemService(repository)
{% endif -%}
