"""Pydantic schemas for API requests/responses."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Base item schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    is_active: bool = True


class ItemCreate(ItemBase):
    """Schema for creating an item."""
    pass


class ItemUpdate(ItemBase):
    """Schema for updating an item."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[float] = Field(None, gt=0)


class ItemResponse(ItemBase):
    """Schema for item response."""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
