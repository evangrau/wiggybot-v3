from mariadb import ConnectionPool
from contextlib import contextmanager
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
from loguru import logger as log

POOL = ConnectionPool(
    pool_name="mypool",
    host=DB_HOST,
    port=int(DB_PORT),
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

@contextmanager
def get_connection():
    """
    Context manager to yield a pooled DB connection.
    Commits on success, rolls back on exception, always closes.
    Logs connection lifecycle events.
    """
    conn = POOL.get_connection()
    log.debug("Acquired DB connection from pool")
    try:
        yield conn
        conn.commit()
        log.debug("Transaction committed successfully")
    except Exception as e:
        conn.rollback()
        log.error(f"Transaction rolled back due to error: {e}")
        raise
    finally:
        conn.close()
        log.debug("DB connection returned to pool")
