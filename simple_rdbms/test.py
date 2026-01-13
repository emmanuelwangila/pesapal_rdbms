from infrastructure.storage.in_memory_storage import InMemoryStorage
from infrastructure.repositories.table_repository import TableRepository
from application.services.crud_service import CrudService
from application.services.query_service import QueryService
from infrastructure.parsers.sql_parser import SqlParser

def test_rdbms():
    storage = InMemoryStorage()
    repo = TableRepository(storage)
    crud = CrudService(repo)
    query_svc = QueryService(crud)
    parser = SqlParser()

    # Test create table
    sql = "CREATE TABLE users (id INTEGER PRIMARY KEY, name VARCHAR UNIQUE, age INTEGER)"
    query = parser.parse(sql)
    query_svc.execute(query)
    print("✓ Table 'users' created successfully")

    # Insert data
    sql = "INSERT INTO users VALUES (1, 'Alice', 30)"
    query = parser.parse(sql)
    query_svc.execute(query)
    print("✓ Data inserted into 'users'")

    # Select all
    sql = "SELECT * FROM users"
    query = parser.parse(sql)
    result = query_svc.execute(query)
    print("✓ Select result:", result)
    assert len(result) == 1
    assert result[0]['name'] == 'Alice'

    # Test unique constraint
    try:
        sql = "INSERT INTO users VALUES (2, 'Alice', 25)"  # Same name
        query = parser.parse(sql)
        query_svc.execute(query)
        assert False, "Should have failed unique constraint"
    except ValueError as e:
        print("✓ Unique constraint enforced:", str(e))

    # Test primary key
    try:
        sql = "INSERT INTO users VALUES (1, 'Bob', 25)"  # Same id
        query = parser.parse(sql)
        query_svc.execute(query)
        assert False, "Should have failed primary key constraint"
    except ValueError as e:
        print("✓ Primary key constraint enforced:", str(e))

    # Create orders table
    sql = "CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, product VARCHAR)"
    query = parser.parse(sql)
    query_svc.execute(query)
    print("✓ Table 'orders' created")

    # Insert order
    sql = "INSERT INTO orders VALUES (1, 1, 'Book')"
    query = parser.parse(sql)
    query_svc.execute(query)
    print("✓ Order inserted")

    # Test join
    sql = "SELECT * FROM users JOIN orders ON users.id = orders.user_id"
    query = parser.parse(sql)
    print("Parsed query:", query)
    result = query_svc.execute(query)
    print("✓ Join result:", result)
    if result:
        print("Keys in result:", list(result[0].keys()))
        assert 'product' in result[0]
        assert result[0]['product'] == 'Book'
    else:
        assert False, "Join should return result"

    # Test update
    sql = "UPDATE users SET age = 31 WHERE id = 1"
    query = parser.parse(sql)
    query_svc.execute(query)
    print("✓ Update executed")

    # Verify update
    sql = "SELECT * FROM users WHERE id = 1"
    query = parser.parse(sql)
    result = query_svc.execute(query)
    assert result[0]['age'] == 31
    print("✓ Update verified")

    # Test delete
    sql = "DELETE FROM users WHERE id = 1"
    query = parser.parse(sql)
    query_svc.execute(query)
    print("✓ Delete executed")

    # Verify delete
    sql = "SELECT * FROM users"
    query = parser.parse(sql)
    result = query_svc.execute(query)
    assert len(result) == 0
    print("✓ Delete verified")

    print("\n🎉 All tests passed! The RDBMS is working correctly.")

if __name__ == "__main__":
    test_rdbms()