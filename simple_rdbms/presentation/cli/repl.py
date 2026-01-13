import cmd
from infrastructure.parsers.sql_parser import SqlParser
from application.services.query_service import QueryService
from application.services.crud_service import CrudService
from infrastructure.repositories.table_repository import TableRepository
from infrastructure.storage.in_memory_storage import InMemoryStorage

class Repl(cmd.Cmd):
    intro = "Welcome to Simple RDBMS. Type SQL commands or 'quit' to exit."
    prompt = "rdbms> "

    def __init__(self):
        super().__init__()
        self.storage = InMemoryStorage()
        self.table_repo = TableRepository(self.storage)
        self.crud_service = CrudService(self.table_repo)
        self.query_service = QueryService(self.crud_service)
        self.parser = SqlParser()

    def default(self, line):
        if line.strip().lower() in ['quit', 'exit']:
            return True
        try:
            query = self.parser.parse(line)
            result = self.query_service.execute(query)
            if result is not None:
                print(result)
            else:
                print("OK")
        except Exception as e:
            print(f"Error: {e}")

    def do_quit(self, line):
        return True

    do_exit = do_quit