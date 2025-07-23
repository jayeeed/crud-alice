import logging
from fastapi import HTTPException
from database import get_db
from models import ItemCreate, ItemUpdate

logger = logging.getLogger(__name__)


class ItemService:
    @staticmethod
    def create_item(item: ItemCreate):
        """Create a new item"""
        logger.info(f"Creating item: {item.dict()}")
        try:
            conn = get_db()
            cur = conn.cursor()
            logger.info(
                f"Executing INSERT with values: user_id={item.user_id}, name={item.name}, price={item.price}"
            )
            cur.execute(
                "INSERT INTO items (user_id, name, price) VALUES (%s, %s, %s) RETURNING *",
                (item.user_id, item.name, item.price),
            )
            new_item = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            logger.info(f"Successfully created item: {new_item}")
            return new_item
        except Exception as e:
            logger.error(f"Database error in create_item: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def get_all_items():
        """Get all items"""
        logger.info("Fetching all items")
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM items")
            items = cur.fetchall()
            cur.close()
            conn.close()
            logger.info(f"Found {len(items)} items")
            return items
        except Exception as e:
            logger.error(f"Database error in get_all_items: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def get_item_by_id(item_id: str):
        """Get item by ID"""
        logger.info(f"Fetching item with ID: {item_id}")
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM items WHERE id = %s", (item_id,))
            item = cur.fetchone()
            cur.close()
            conn.close()
            if not item:
                logger.warning(f"Item not found with ID: {item_id}")
                raise HTTPException(status_code=404, detail="Item not found")
            logger.info(f"Found item: {item}")
            return item
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Database error in get_item_by_id: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def update_item(item_id: str, item: ItemUpdate, method: str = "PUT"):
        """Update item (works for both PUT and PATCH)"""
        logger.info(f"{method} item {item_id} with data: {item.dict()}")
        try:
            conn = get_db()
            cur = conn.cursor()

            # Build dynamic update query
            updates = []
            values = []
            if item.user_id is not None:
                updates.append("user_id = %s")
                values.append(item.user_id)
            if item.name is not None:
                updates.append("name = %s")
                values.append(item.name)
            if item.price is not None:
                updates.append("price = %s")
                values.append(item.price)

            if not updates:
                logger.warning(f"No fields provided for {method.lower()}")
                raise HTTPException(status_code=400, detail="No fields to update")

            values.append(item_id)
            query = f"UPDATE items SET {', '.join(updates)} WHERE id = %s RETURNING *"
            logger.info(f"Executing query: {query} with values: {values}")

            cur.execute(query, values)
            updated_item = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()

            if not updated_item:
                logger.warning(
                    f"Item not found for {method.lower()} with ID: {item_id}"
                )
                raise HTTPException(status_code=404, detail="Item not found")

            logger.info(f"Successfully {method.lower()}ed item: {updated_item}")
            return updated_item
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Database error in update_item: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def delete_item(item_id: str):
        """Delete item by ID"""
        logger.info(f"Deleting item with ID: {item_id}")
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM items WHERE id = %s RETURNING *", (item_id,))
            deleted_item = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()

            if not deleted_item:
                logger.warning(f"Item not found for deletion with ID: {item_id}")
                raise HTTPException(status_code=404, detail="Item not found")

            logger.info(f"Successfully deleted item: {deleted_item}")
            return {"message": "Item deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Database error in delete_item: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
