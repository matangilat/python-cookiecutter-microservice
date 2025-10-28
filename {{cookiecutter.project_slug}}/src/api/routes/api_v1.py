"""API routes for FastAPI."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.models.schemas import ItemCreate, ItemResponse
from src.services.item_service import ItemService
from src.dependencies import get_item_service

router = APIRouter()


@router.get("/items", response_model=List[ItemResponse])
async def list_items(
    skip: int = 0,
    limit: int = 100,
    service: ItemService = Depends(get_item_service)
):
    """List all items."""
    return await service.list_items(skip=skip, limit=limit)


@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    service: ItemService = Depends(get_item_service)
):
    """Create a new item."""
    return await service.create_item(item)


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: str,
    service: ItemService = Depends(get_item_service)
):
    """Get item by ID."""
    item = await service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: str,
    item: ItemCreate,
    service: ItemService = Depends(get_item_service)
):
    """Update an item."""
    updated = await service.update_item(item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: str,
    service: ItemService = Depends(get_item_service)
):
    """Delete an item."""
    deleted = await service.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
