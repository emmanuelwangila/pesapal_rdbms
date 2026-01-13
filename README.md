# Simple RDBMS

A simple relational database management system implemented in Python following clean architecture principles.

## Features

- Support for tables with columns of INTEGER, VARCHAR, BOOLEAN, FLOAT types
- CRUD operations (Create, Read, Update, Delete)
- Primary key and unique constraints
- Basic indexing for fast lookups
- Basic inner joins
- SQL-like interface with support for CREATE TABLE, INSERT, SELECT, UPDATE, DELETE
- Interactive REPL mode
- Simple web interface for executing queries

## Architecture

The project follows Clean Architecture with the following layers:

- **Domain**: Core business entities (Table, Column, DataType)
- **Application**: Services for CRUD and query execution
- **Infrastructure**: Storage, repositories, and SQL parser
- **Presentation**: CLI REPL and web interface

## Installation

1. Ensure Python 3.8+ is installed
2. Install dependencies: `pip install -r requirements.txt`

## Usage

### REPL Mode

Run `python main.py` to start the interactive REPL.

Example commands:

```
CREATE TABLE users (id INTEGER PRIMARY KEY, name VARCHAR UNIQUE, age INTEGER);
INSERT INTO users VALUES (1, 'Alice', 30);
INSERT INTO users VALUES (2, 'Bob', 25);
SELECT * FROM users;
SELECT * FROM users WHERE id = 1;
UPDATE users SET age = 31 WHERE id = 1;
DELETE FROM users WHERE id = 2;
CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, product VARCHAR);
INSERT INTO orders VALUES (1, 1, 'Book');
SELECT * FROM users JOIN orders ON users.id = orders.user_id;
```

### Web Interface

Run `python presentation/web/app.py` to start the web server.

Visit `http://localhost:5000` in your browser to access the simple web interface for executing SQL queries.

## Demonstration Web App

The web interface serves as a trivial demonstration of using the RDBMS for CRUD operations. You can create tables, insert data, and query it through the web form.

## Limitations

- In-memory storage (data is lost on restart)
- Simple WHERE clauses only (equality)
- No transactions or concurrency
- Basic joins only (inner join with equality)

This implementation is for educational purposes and demonstrates the core concepts of a RDBMS.
