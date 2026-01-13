from typing import List
from domain.entities.table import Table
from infrastructure.storage.in_memory_storage import InMemoryStorage

class TableRepository:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def save(self, table: Table):
        self.storage.create_table(table)

    def find_by_name(self, name: str) -> Table:
        return self.storage.get_table(name)

    def delete(self, name: str):
        self.storage.drop_table(name)

    def find_all_names(self) -> List[str]:
        return self.storage.list_tables()