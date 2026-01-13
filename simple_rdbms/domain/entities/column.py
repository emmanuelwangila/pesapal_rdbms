from domain.value_objects.data_type import DataType

class Column:
    def __init__(self, name: str, data_type: DataType, primary_key: bool = False, unique: bool = False, nullable: bool = True):
        self.name = name
        self.data_type = data_type
        self.primary_key = primary_key
        self.unique = unique
        self.nullable = nullable

    def validate_value(self, value):
        if value is None and not self.nullable:
            raise ValueError(f"Column {self.name} cannot be null")
        if self.data_type == DataType.INTEGER:
            if not isinstance(value, int) and value is not None:
                raise ValueError(f"Value for {self.name} must be integer")
        elif self.data_type == DataType.VARCHAR:
            if not isinstance(value, str) and value is not None:
                raise ValueError(f"Value for {self.name} must be string")
        elif self.data_type == DataType.BOOLEAN:
            if not isinstance(value, bool) and value is not None:
                raise ValueError(f"Value for {self.name} must be boolean")
        elif self.data_type == DataType.FLOAT:
            if not isinstance(value, (int, float)) and value is not None:
                raise ValueError(f"Value for {self.name} must be number")