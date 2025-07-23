import logging
from fastapi import APIRouter
from models import ItemCreate, ItemUpdate
from services import ItemService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
async def root():
    logger.info("GET / - Root endpoint accessed")
    return {"message": "CRUD API is running", "endpoints": ["/items", "/docs"]}


@router.post("/test")
async def test_item(item: ItemCreate):
    logger.info(f"POST /test - Received item: {item.dict()}")
    return {"received": item.dict(), "message": "Data validation successful"}


@router.post("/items")
async def create_item(item: ItemCreate):
    logger.info(f"POST /items - Creating item")
    return ItemService.create_item(item)


@router.get("/items")
async def get_items():
    logger.info("GET /items - Fetching all items")
    return ItemService.get_all_items()


@router.get("/items/{item_id}")
async def get_item(item_id: str):
    logger.info(f"GET /items/{item_id} - Fetching item")
    return ItemService.get_item_by_id(item_id)


@router.put("/items/{item_id}")
async def update_item(item_id: str, item: ItemUpdate):
    logger.info(f"PUT /items/{item_id} - Updating item")
    return ItemService.update_item(item_id, item, "PUT")


@router.patch("/items/{item_id}")
async def patch_item(item_id: str, item: ItemUpdate):
    logger.info(f"PATCH /items/{item_id} - Patching item")
    return ItemService.update_item(item_id, item, "PATCH")


@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    logger.info(f"DELETE /items/{item_id} - Deleting item")
    return ItemService.delete_item(item_id)
