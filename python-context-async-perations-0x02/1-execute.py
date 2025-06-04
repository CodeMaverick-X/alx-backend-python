import sqlite3


class ExecuteQuery:
    def __init__(self, age):
        self.age = age
        
    def __enter__(self):
        self._conn =  sqlite3.connect('users.db')
        cursor = self._conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE age > {self.age}")
        self._rows = cursor.fetchall()
        return self._rows
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._conn.close()
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        return True        
    
    
with ExecuteQuery(30) as rows:
    for row in rows:
        print(row)