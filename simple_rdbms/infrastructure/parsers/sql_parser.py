import re
from typing import Dict, Any, List
from domain.value_objects.data_type import DataType

class SqlParser:
    def parse(self, sql: str) -> Dict[str, Any]:
        sql = sql.strip()
        if sql.upper().startswith("CREATE TABLE"):
            return self._parse_create_table(sql)
        elif sql.upper().startswith("INSERT INTO"):
            return self._parse_insert(sql)
        elif sql.upper().startswith("SELECT"):
            return self._parse_select(sql)
        elif sql.upper().startswith("UPDATE"):
            return self._parse_update(sql)
        elif sql.upper().startswith("DELETE FROM"):
            return self._parse_delete(sql)
        else:
            raise ValueError("Unsupported SQL statement")

    def _parse_create_table(self, sql: str) -> Dict[str, Any]:
        # CREATE TABLE table_name (col_def, ...)
        match = re.match(r"CREATE TABLE (\w+)\s*\((.+)\)", sql, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid CREATE TABLE syntax")
        table_name = match.group(1)
        col_defs_str = match.group(2)
        columns = []
        for col_def_str in col_defs_str.split(','):
            col_def_str = col_def_str.strip()
            parts = col_def_str.split()
            name = parts[0]
            type_str = parts[1].upper()
            primary_key = "PRIMARY KEY" in col_def_str.upper()
            unique = "UNIQUE" in col_def_str.upper()
            data_type = DataType(type_str)
            columns.append({
                'name': name,
                'type': type_str,
                'primary_key': primary_key,
                'unique': unique
            })
        return {
            'type': 'create_table',
            'name': table_name,
            'columns': columns
        }

    def _parse_insert(self, sql: str) -> Dict[str, Any]:
        # INSERT INTO table VALUES (val1, val2, ...)
        match = re.match(r"INSERT INTO (\w+)\s+VALUES\s*\((.+)\)", sql, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid INSERT syntax")
        table_name = match.group(1)
        values_str = match.group(2)
        values = [self._parse_value(v.strip()) for v in values_str.split(',')]
        # Assume order matches columns
        return {
            'type': 'insert',
            'table': table_name,
            'values': values  # list of values
        }

    def _parse_select(self, sql: str) -> Dict[str, Any]:
        # SELECT * FROM table [JOIN table2 ON col1 = col2] [WHERE col = val]
        match = re.match(r"SELECT (.+) FROM (\w+)(?:\s+JOIN (\w+) ON (.+?))?(?:\s+WHERE (.+))?", sql, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid SELECT syntax")
        columns_str = match.group(1).strip()
        table_name = match.group(2)
        join_table = match.group(3)
        on_condition = match.group(4)
        where_str = match.group(5)
        columns = [c.strip() for c in columns_str.split(',')] if columns_str != '*' else ['*']
        join = None
        if join_table and on_condition:
            # Simple: col1 = col2
            on_match = re.match(r"(.+)\s*=\s*(.+)", on_condition.strip())
            if on_match:
                left = on_match.group(1).strip()
                right = on_match.group(2).strip()
                join = {'table': join_table, 'on': {'left': left, 'right': right}}
        where = None
        if where_str:
            where_match = re.match(r"(\w+)\s*=\s*(.+)", where_str.strip())
            if where_match:
                col = where_match.group(1)
                val = self._parse_value(where_match.group(2).strip())
                where = {col: val}
        return {
            'type': 'select',
            'table': table_name,
            'columns': columns,
            'join': join,
            'where': where
        }

    def _parse_update(self, sql: str) -> Dict[str, Any]:
        # UPDATE table SET col = val WHERE pk = val
        match = re.match(r"UPDATE (\w+)\s+SET (.+)\s+WHERE (.+)", sql, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid UPDATE syntax")
        table_name = match.group(1)
        set_str = match.group(2)
        where_str = match.group(3)
        updates = {}
        for assign in set_str.split(','):
            assign = assign.strip()
            col, val_str = assign.split('=')
            col = col.strip()
            val = self._parse_value(val_str.strip())
            updates[col] = val
        # Assume where is pk = val
        where_match = re.match(r"(\w+)\s*=\s*(.+)", where_str.strip())
        pk_col = where_match.group(1)
        pk_val = self._parse_value(where_match.group(2).strip())
        return {
            'type': 'update',
            'table': table_name,
            'updates': updates,
            'pk_col': pk_col,
            'pk_val': pk_val
        }

    def _parse_delete(self, sql: str) -> Dict[str, Any]:
        # DELETE FROM table WHERE pk = val
        match = re.match(r"DELETE FROM (\w+)\s+WHERE (.+)", sql, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid DELETE syntax")
        table_name = match.group(1)
        where_str = match.group(2)
        where_match = re.match(r"(\w+)\s*=\s*(.+)", where_str.strip())
        pk_col = where_match.group(1)
        pk_val = self._parse_value(where_match.group(2).strip())
        return {
            'type': 'delete',
            'table': table_name,
            'pk_col': pk_col,
            'pk_val': pk_val
        }

    def _parse_value(self, val_str: str):
        val_str = val_str.strip()
        if val_str.startswith("'") and val_str.endswith("'"):
            return val_str[1:-1]
        elif val_str.lower() == 'true':
            return True
        elif val_str.lower() == 'false':
            return False
        elif '.' in val_str:
            return float(val_str)
        else:
            return int(val_str)