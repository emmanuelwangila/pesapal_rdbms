from typing import List, Dict, Any
from domain.entities.column import Column

class Table:
    def __init__(self, name: str, columns: List[Column]):
        self.name = name
        self.columns = columns
        self.rows: List[Dict[str, Any]] = []
        self.primary_key_index: Dict[Any, int] = {}
        self.unique_indexes: Dict[str, set] = {}
        self.column_map = {col.name: col for col in columns}

        # Setup indexes
        for col in columns:
            if col.primary_key:
                self.primary_key_index = {}
            if col.unique:
                self.unique_indexes[col.name] = set()

    def insert_row(self, row_dict: Dict[str, Any]):
        # Validate
        for col_name, value in row_dict.items():
            if col_name not in self.column_map:
                raise ValueError(f"Unknown column {col_name}")
            self.column_map[col_name].validate_value(value)

        # Check primary key
        pk_col = next((col for col in self.columns if col.primary_key), None)
        if pk_col and row_dict.get(pk_col.name) in self.primary_key_index:
            raise ValueError("Primary key violation")

        # Check uniques
        for col_name, unique_set in self.unique_indexes.items():
            value = row_dict.get(col_name)
            if value in unique_set:
                raise ValueError(f"Unique constraint violation for {col_name}")

        # Insert
        self.rows.append(row_dict)

        # Update indexes
        if pk_col:
            self.primary_key_index[row_dict[pk_col.name]] = len(self.rows) - 1
        for col_name in self.unique_indexes:
            self.unique_indexes[col_name].add(row_dict.get(col_name))

    def get_row_by_pk(self, pk_value):
        if self.primary_key_index:
            idx = self.primary_key_index.get(pk_value)
            if idx is not None:
                return self.rows[idx]
        return None

    def update_row(self, pk_value, updates: Dict[str, Any]):
        row = self.get_row_by_pk(pk_value)
        if row is None:
            raise ValueError("Row not found")
        for col_name, value in updates.items():
            if col_name not in self.column_map:
                raise ValueError(f"Unknown column {col_name}")
            self.column_map[col_name].validate_value(value)
        row.update(updates)

    def delete_row(self, pk_value):
        pk_col = next((col for col in self.columns if col.primary_key), None)
        if pk_col and pk_value in self.primary_key_index:
            idx = self.primary_key_index[pk_value]
            del self.rows[idx]
            del self.primary_key_index[pk_value]
            # Rebuild unique indexes
            for col_name in self.unique_indexes:
                self.unique_indexes[col_name] = set(row.get(col_name) for row in self.rows)

    def select_rows(self, where_clause=None):
        if where_clause is None:
            return self.rows
        # where_clause is dict of col: value
        return [row for row in self.rows if all(row.get(k) == v for k, v in where_clause.items())]