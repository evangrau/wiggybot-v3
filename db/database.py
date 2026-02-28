import random
import pandas as pd
from db.database_connection import get_connection
from loguru import logger as log

def get_sql(name : str) -> str:
    """Get the SQL query from the sql folder."""
    try:
        with open(f"sql/{name}.sql", "r") as f:
            sql = f.read()
            log.info(f"Successfully read SQL query from sql/{name}.sql.")
            return sql
    except Exception as e:
        log.error(f"An error occurred while reading SQL query from sql/{name}.sql: {e}")

def get_all_cracked_records() -> pd.DataFrame:
    """Get all records from the cracked table."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            sql = get_sql("get_all_cracked_records")
            cursor.execute(sql)
            records = cursor.fetchall()
            df = pd.DataFrame(records, columns=[desc[0] for desc in cursor.description])
            log.info(f"Successfully retrieved all records from the cracked table.")
            return df
    except Exception as e:
        log.error(f"An error occurred while retrieving records from the cracked table: {e}")
        return pd.DataFrame()

def update_record(table: str, discord_id: int, updates: dict):
    """Update a record in the specified table."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
            sql = f"UPDATE {table} SET {set_clause} WHERE discord_id = %s"
            values = list(updates.values()) + [discord_id]
            cursor.execute(sql, values)
            log.info(f"Successfully updated record for discord_id {discord_id} in table {table} with updates: {updates}.")
    except Exception as e:
        log.error(f"An error occurred while updating record for discord_id {discord_id} in table {table}: {e}")

def create_record(table: str, record: dict):
    """Create a record in the specified table."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            columns = ", ".join(record.keys())
            placeholders = ", ".join(["%s"] * len(record))
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            values = list(record.values())
            cursor.execute(sql, values)
            log.info(f"Successfully created record in table {table} with values: {record}.")
    except Exception as e:
        log.error(f"An error occurred while creating record in table {table} with values {record}: {e}")

def get_number_of_records_from_table(table: str) -> int:
    """Get the number of records in the specified table."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            sql = f"SELECT COUNT(*) FROM {table}"
            cursor.execute(sql)
            count = cursor.fetchone()[0]
            log.info(f"Successfully retrieved the number of records from table {table}: {count}.")
            return count
    except Exception as e:
        log.error(f"An error occurred while retrieving the number of records from table {table}: {e}")
        return 0

def get_random_quote() -> pd.DataFrame:
    """Get a random quote from the database."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            sql = get_sql("get_quote_by_id")
            cursor.execute(sql, {"id": random.randint(1, get_number_of_records_from_table('quotes'))})
            record = cursor.fetchone()
            df = pd.DataFrame([record], columns=[desc[0] for desc in cursor.description])
            log.info(f"Successfully retrieved a random quote from the database: {record}.")
            return df
    except Exception as e:
        log.error(f"An error occurred while retrieving a random quote from the database: {e}")
        return pd.DataFrame()
