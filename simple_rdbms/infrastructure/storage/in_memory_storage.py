from typing import Dict
from domain.entities.table import Table

class InMemoryStorage:
    def __init__(self):
        self.tables: Dict[str, Table] = {}

    def create_table(self, table: Table):
        if table.name in self.tables:
            raise ValueError("Table already exists")
        self.tables[table.name] = table

    def get_table(self, name: str) -> Table:
        return self.tables.get(name)

    def drop_table(self, name: str):
        if name in self.tables:
            del self.tables[name]

    def list_tables(self):
        return list(self.tables.keys())