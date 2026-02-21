from pyairtable import Api
import settings
import pandas as pd
from loguru import logger as log

ID = settings.AIRTABLE_DB

class DBConnection:
    
    def get_table(self, table: str) -> Api.table:
        api = Api(settings.AIRTABLE_API_SECRET)
        log.debug(f"Getting table '{table}' from Airtable database with ID '{ID}'.")
        return api.table(ID, table)
    
    def get_all_records(self, table: str) -> pd.DataFrame:
        log.debug(f"Retrieving all records from table '{table}' in Airtable database with ID '{ID}'.")
        records = self.get_table(table).all()
        return pd.json_normalize(records)
    
    def create_record(self, table: str, record: dict):
        log.debug(f"Creating a new record in table '{table}' in Airtable database with ID '{ID}': {record}")
        self.get_table(table).create(record)

    def find_record_by_username(self, table: str, username: str) -> str:
        log.debug(f"Searching for record with username '{username}' in table '{table}' in Airtable database with ID '{ID}'.")
        records = self.get_table(table).all(formula=f"{{username}}='{username}'")
        return records[0]['fields']['record_id'] if records else None
    
    def update_record_using_username(self, table: str, username: str, fields: dict):
        record_id = self.find_record_by_username(table, username)
        if record_id:
            log.debug(f"Updating record with username '{username}' in table '{table}' in Airtable database with ID '{ID}': {fields}")
            self.get_table(table).update(record_id, fields)
        else:
            raise ValueError(f"Record with username '{username}' not found in table '{table}'.")
    
    def update_record(self, table: str, record_id: str, fields: dict):
        log.debug(f"Updating record with ID '{record_id}' in table '{table}' in Airtable database with ID '{ID}': {fields}")
        self.get_table(table).update(record_id, fields)

    def delete_record(self, table: str, record_id: str):
        log.debug(f"Deleting record with ID '{record_id}' from table '{table}' in Airtable database with ID '{ID}'.")
        self.get_table(table).delete(record_id)
