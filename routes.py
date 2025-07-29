import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import ItemCreate, ItemUpdate
from services import ItemService
from database import get_db

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
async def root():
    logger.info("GET / - Root endpoint accessed")
    return {"message": "CRUD API is running", "endpoints": ["/items", "/docs"]}


@router.post("/items")
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    logger.info(f"POST /items - Creating item")
    return ItemService.create_item(item, db)


@router.get("/items")
async def get_items(db: Session = Depends(get_db)):
    logger.info("GET /items - Fetching all items")
    return ItemService.get_all_items(db)


@router.get("/items/{item_id}")
async def get_item(item_id: str, db: Session = Depends(get_db)):
    logger.info(f"GET /items/{item_id} - Fetching item")
    return ItemService.get_item_by_id(item_id, db)


@router.put("/items/{item_id}")
async def update_item(item_id: str, item: ItemUpdate, db: Session = Depends(get_db)):
    logger.info(f"PUT /items/{item_id} - Updating item")
    return ItemService.update_item(item_id, item, db, "PUT")


@router.patch("/items/{item_id}")
async def patch_item(item_id: str, item: ItemUpdate, db: Session = Depends(get_db)):
    logger.info(f"PATCH /items/{item_id} - Patching item")
    return ItemService.update_item(item_id, item, db, "PATCH")


@router.delete("/items/{item_id}")
async def delete_item(item_id: str, db: Session = Depends(get_db)):
    logger.info(f"DELETE /items/{item_id} - Deleting item")
    return ItemService.delete_item(item_id, db)
