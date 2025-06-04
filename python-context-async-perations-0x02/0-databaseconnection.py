import time
import sqlite3
import functools

class DatabaseConnection:
    def __init__(self):
        self._conn = None
    
    def __enter__(self):
        print("Opening database connection")
        self._conn =  sqlite3.connect('users.db')
        return "Database Connection"
    def __exit__(self, exc_type, exc_value, traceback):
        print("Closing database connection")
        self._conn.close()
        return True
    
    
    
    
with DatabaseConnection() as db:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")