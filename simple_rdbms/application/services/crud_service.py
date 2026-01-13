from typing import List, Dict, Any
from domain.entities.table import Table
from domain.entities.column import Column
from infrastructure.repositories.table_repository import TableRepository

class CrudService:
    def __init__(self, table_repo: TableRepository):
        self.table_repo = table_repo

    def create_table(self, name: str, columns: List[Column]):
        table = Table(name, columns)
        self.table_repo.save(table)

    def insert(self, table_name: str, row: Dict[str, Any]):
        table = self.table_repo.find_by_name(table_name)
        if not table:
            raise ValueError("Table not found")
        table.insert_row(row)

    def select(self, table_name: str, where=None):
        table = self.table_repo.find_by_name(table_name)
        if not table:
            raise ValueError("Table not found")
        return table.select_rows(where)

    def update(self, table_name: str, pk_value, updates: Dict[str, Any]):
        table = self.table_repo.find_by_name(table_name)
        if not table:
            raise ValueError("Table not found")
        table.update_row(pk_value, updates)

    def delete(self, table_name: str, pk_value):
        table = self.table_repo.find_by_name(table_name)
        if not table:
            raise ValueError("Table not found")
        table.delete_row(pk_value)