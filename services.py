import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database import Item
from models import ItemCreate, ItemUpdate
import uuid

logger = logging.getLogger(__name__)


class ItemService:
    @staticmethod
    def create_item(item: ItemCreate, db: Session):
        """Create a new item"""
        logger.info(f"Creating item: {item.dict()}")
        try:
            logger.info(
                f"Creating item with values: user_id={item.user_id}, name={item.name}, price={item.price}"
            )
            db_item = Item(user_id=item.user_id, name=item.name, price=item.price)
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            logger.info(f"Successfully created item: {db_item.id}")
            return {
                "id": str(db_item.id),
                "user_id": db_item.user_id,
                "name": db_item.name,
                "price": db_item.price,
            }
        except Exception as e:
            db.rollback()
            logger.error(f"Database error in create_item: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def get_all_items(db: Session):
        """Get all items"""
        logger.info("Fetching all items")
        try:
            items = db.query(Item).all()
            logger.info(f"Found {len(items)} items")
            return [
                {
                    "id": str(item.id),
                    "user_id": item.user_id,
                    "name": item.name,
                    "price": item.price,
                }
                for item in items
            ]
        except Exception as e:
            logger.error(f"Database error in get_all_items: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def get_item_by_id(item_id: str, db: Session):
        """Get item by ID"""
        logger.info(f"Fetching item with ID: {item_id}")
        try:
            item = db.query(Item).filter(Item.id == uuid.UUID(item_id)).first()
            if not item:
                logger.warning(f"Item not found with ID: {item_id}")
                raise HTTPException(status_code=404, detail="Item not found")
            logger.info(f"Found item: {item.id}")
            return {
                "id": str(item.id),
                "user_id": item.user_id,
                "name": item.name,
                "price": item.price,
            }
        except ValueError:
            logger.warning(f"Invalid UUID format: {item_id}")
            raise HTTPException(status_code=400, detail="Invalid ID format")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Database error in get_item_by_id: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def update_item(
        item_id: str, item_update: ItemUpdate, db: Session, method: str = "PUT"
    ):
        """Update item (works for both PUT and PATCH)"""
        logger.info(f"{method} item {item_id} with data: {item_update.dict()}")
        try:
            db_item = db.query(Item).filter(Item.id == uuid.UUID(item_id)).first()
            if not db_item:
                logger.warning(
                    f"Item not found for {method.lower()} with ID: {item_id}"
                )
                raise HTTPException(status_code=404, detail="Item not found")

            # Update only provided fields
            update_data = item_update.dict(exclude_unset=True)
            if not update_data:
                logger.warning(f"No fields provided for {method.lower()}")
                raise HTTPException(status_code=400, detail="No fields to update")

            for field, value in update_data.items():
                setattr(db_item, field, value)

            db.commit()
            db.refresh(db_item)
            logger.info(f"Successfully {method.lower()}ed item: {db_item.id}")
            return {
                "id": str(db_item.id),
                "user_id": db_item.user_id,
                "name": db_item.name,
                "price": db_item.price,
            }
        except ValueError:
            logger.warning(f"Invalid UUID format: {item_id}")
            raise HTTPException(status_code=400, detail="Invalid ID format")
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Database error in update_item: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def delete_item(item_id: str, db: Session):
        """Delete item by ID"""
        logger.info(f"Deleting item with ID: {item_id}")
        try:
            db_item = db.query(Item).filter(Item.id == uuid.UUID(item_id)).first()
            if not db_item:
                logger.warning(f"Item not found for deletion with ID: {item_id}")
                raise HTTPException(status_code=404, detail="Item not found")

            db.delete(db_item)
            db.commit()
            logger.info(f"Successfully deleted item: {item_id}")
            return {"message": "Item deleted successfully"}
        except ValueError:
            logger.warning(f"Invalid UUID format: {item_id}")
            raise HTTPException(status_code=400, detail="Invalid ID format")
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Database error in delete_item: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
