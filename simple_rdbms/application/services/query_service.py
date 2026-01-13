from typing import Dict, Any, List
from domain.value_objects.data_type import DataType
from domain.entities.column import Column
from application.services.crud_service import CrudService

class QueryService:
    def __init__(self, crud_service: CrudService):
        self.crud = crud_service

    def execute(self, query: Dict[str, Any]) -> Any:
        if query['type'] == 'create_table':
            columns = []
            for col_def in query['columns']:
                dt = DataType(col_def['type'])
                col = Column(col_def['name'], dt, col_def['primary_key'], col_def['unique'])
                columns.append(col)
            self.crud.create_table(query['name'], columns)
        elif query['type'] == 'insert':
            table = self.crud.table_repo.find_by_name(query['table'])
            row_dict = {}
            for i, val in enumerate(query['values']):
                col = table.columns[i]
                row_dict[col.name] = val
            self.crud.insert(query['table'], row_dict)
        elif query['type'] == 'select':
            if query.get('join'):
                # Perform join
                rows1 = self.crud.select(query['table'])
                rows2 = self.crud.select(query['join']['table'])
                joined = []
                left_col = query['join']['on']['left']
                right_col = query['join']['on']['right']
                # Assume no table prefix for simplicity
                left_key = left_col.split('.')[1] if '.' in left_col else left_col
                right_key = right_col.split('.')[1] if '.' in right_col else right_col
                for r1 in rows1:
                    for r2 in rows2:
                        if r1.get(left_key) == r2.get(right_key):
                            # Merge rows carefully to preserve both tables' fields.
                            merged = {}
                            for k, v in r1.items():
                                merged[k] = v
                            for k, v in r2.items():
                                if k in merged:
                                    # avoid clobbering keys from the left table
                                    merged[f"{query['join']['table']}_{k}"] = v
                                else:
                                    merged[k] = v
                            joined.append(merged)
                rows = joined
            else:
                rows = self.crud.select(query['table'], query.get('where'))
            if query.get('where') and query.get('join'):
                # Apply where after join
                rows = [r for r in rows if all(r.get(k) == v for k, v in query['where'].items())]
            if query['columns'] == ['*']:
                return rows
            else:
                return [{k: r[k] for k in query['columns'] if k in r} for r in rows]
        elif query['type'] == 'update':
            self.crud.update(query['table'], query['pk_val'], query['updates'])
        elif query['type'] == 'delete':
            self.crud.delete(query['table'], query['pk_val'])
        return None