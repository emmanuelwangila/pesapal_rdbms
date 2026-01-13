from flask import Flask, request, jsonify
from infrastructure.parsers.sql_parser import SqlParser
from application.services.query_service import QueryService
from application.services.crud_service import CrudService
from infrastructure.repositories.table_repository import TableRepository
from infrastructure.storage.in_memory_storage import InMemoryStorage

app = Flask(__name__)

storage = InMemoryStorage()
table_repo = TableRepository(storage)
crud_service = CrudService(table_repo)
query_service = QueryService(crud_service)
parser = SqlParser()

@app.route('/query', methods=['GET'])
def query():
    sql = request.args.get('sql')
    if not sql:
        return jsonify({'error': 'No SQL provided'}), 400
    try:
        query = parser.parse(sql)
        result = query_service.execute(query)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def index():
    return """
    <html>
    <body>
    <h1>Simple RDBMS Web Interface</h1>
    <form action="/query" method="get">
        <input type="text" name="sql" placeholder="Enter SQL here" size="50"><br>
        <input type="submit" value="Execute">
    </form>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)