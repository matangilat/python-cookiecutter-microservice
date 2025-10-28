"""API routes for Flask."""
from flask import Blueprint, jsonify, request, current_app
import asyncio
from functools import wraps

from src.models.schemas import ItemCreate
from src.services.item_service import ItemService
from src.dependencies import get_item_service_flask

api_bp = Blueprint("api", __name__)


def async_route(f):
    """Decorator to run async functions in Flask routes."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(f(*args, **kwargs))
        finally:
            loop.close()
    return wrapper


@api_bp.route("/items", methods=["GET"])
@async_route
async def list_items():
    """List all items."""
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 100, type=int)
    
    service = await get_item_service_flask()
    items = await service.list_items(skip=skip, limit=limit)
    
    return jsonify([item.dict() for item in items])


@api_bp.route("/items", methods=["POST"])
@async_route
async def create_item():
    """Create a new item."""
    data = request.get_json()
    item_create = ItemCreate(**data)
    
    service = await get_item_service_flask()
    item = await service.create_item(item_create)
    
    return jsonify(item.dict()), 201


@api_bp.route("/items/<item_id>", methods=["GET"])
@async_route
async def get_item(item_id):
    """Get item by ID."""
    service = await get_item_service_flask()
    item = await service.get_item(item_id)
    
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify(item.dict())


@api_bp.route("/items/<item_id>", methods=["PUT"])
@async_route
async def update_item(item_id):
    """Update an item."""
    data = request.get_json()
    item_update = ItemCreate(**data)
    
    service = await get_item_service_flask()
    item = await service.update_item(item_id, item_update)
    
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify(item.dict())


@api_bp.route("/items/<item_id>", methods=["DELETE"])
@async_route
async def delete_item(item_id):
    """Delete an item."""
    service = await get_item_service_flask()
    deleted = await service.delete_item(item_id)
    
    if not deleted:
        return jsonify({"error": "Item not found"}), 404
    
    return "", 204
