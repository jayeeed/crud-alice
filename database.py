import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from config import DATABASE_URL

logger = logging.getLogger(__name__)


def get_db():
    """Get database connection"""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_database():
    """Initialize database table"""
    logger.info("Initializing database...")
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            price TEXT NOT NULL
        )
    """
    )
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Database initialized successfully")
