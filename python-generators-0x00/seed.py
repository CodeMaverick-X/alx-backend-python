#!/usr/bin/env python3
"""
Database seeding script for ALX_prodev MySQL database.
Creates database, table structure, and populates with CSV data.
"""

import mysql.connector
from mysql.connector import Error
import csv
import uuid
import os


def connect_db():
    """
    Connects to the MySQL database server.
    
    Returns:
        connection: MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='reinhard',  # Change as needed
            password='plokijuhyg',  # Add your MySQL password here
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        
        if connection.is_connected():
            print("Successfully connected to MySQL server")
            return connection
            
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        
        # Check if database exists
        cursor.execute("SHOW DATABASES LIKE 'ALX_prodev'")
        result = cursor.fetchone()
        
        if not result:
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE ALX_prodev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("Database ALX_prodev created successfully")
        else:
            print("Database ALX_prodev already exists")
            
        cursor.close()
        
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    
    Returns:
        connection: MySQL connection object to ALX_prodev database or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Change as needed
            password='',  # Add your MySQL password here
            database='ALX_prodev',
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        
        if connection.is_connected():
            print("Successfully connected to ALX_prodev database")
            return connection
            
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.
    
    Args:
        connection: MySQL connection object to ALX_prodev database
    """
    try:
        cursor = connection.cursor()
        
        # Check if table exists
        cursor.execute("SHOW TABLES LIKE 'user_data'")
        result = cursor.fetchone()
        
        if not result:
            # Create table with specified schema
            create_table_query = """
            CREATE TABLE user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3,0) NOT NULL,
                INDEX idx_user_id (user_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            
            cursor.execute(create_table_query)
            print("Table user_data created successfully")
        else:
            print("Table user_data already exists")
            
        cursor.close()
        
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file_path):
    """
    Inserts data from CSV file into the database if it does not exist.
    
    Args:
        connection: MySQL connection object to ALX_prodev database
        csv_file_path: Path to the CSV file containing user data
    """
    try:
        cursor = connection.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"Data already exists in user_data table ({count} records)")
            cursor.close()
            return
        
        # Check if CSV file exists
        if not os.path.exists(csv_file_path):
            print(f"CSV file {csv_file_path} not found")
            cursor.close()
            return
        
        # Read and insert data from CSV
        inserted_count = 0
        
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            
            # Prepare insert statement
            insert_query = """
            INSERT IGNORE INTO user_data (user_id, name, email, age) 
            VALUES (%s, %s, %s, %s)
            """
            
            batch_data = []
            batch_size = 1000  # Process in batches for better performance
            
            for row in csv_reader:
                try:
                    # Generate UUID if not provided or validate existing UUID
                    if 'user_id' in row and row['user_id']:
                        user_id = row['user_id']
                        # Validate UUID format
                        uuid.UUID(user_id)
                    else:
                        user_id = str(uuid.uuid4())
                    
                    # Validate and clean data
                    name = row.get('name', '').strip()
                    email = row.get('email', '').strip()
                    age = int(float(row.get('age', 0)))
                    
                    # Skip invalid records
                    if not name or not email or age <= 0:
                        print(f"Skipping invalid record: {row}")
                        continue
                    
                    batch_data.append((user_id, name, email, age))
                    
                    # Insert batch when it reaches batch_size
                    if len(batch_data) >= batch_size:
                        cursor.executemany(insert_query, batch_data)
                        connection.commit()
                        inserted_count += len(batch_data)
                        batch_data = []
                        
                except (ValueError, TypeError, uuid.UUID) as e:
                    print(f"Error processing row {row}: {e}")
                    continue
            
            # Insert remaining records
            if batch_data:
                cursor.executemany(insert_query, batch_data)
                connection.commit()
                inserted_count += len(batch_data)
        
        print(f"Successfully inserted {inserted_count} records into user_data table")
        cursor.close()
        
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    except FileNotFoundError:
        print(f"CSV file {csv_file_path} not found")
    except Exception as e:
        print(f"Unexpected error: {e}")


def validate_database_setup():
    """
    Utility function to validate the database setup.
    
    Returns:
        bool: True if setup is valid, False otherwise
    """
    try:
        connection = connect_to_prodev()
        if not connection:
            return False
        
        cursor = connection.cursor()
        
        # Check database exists
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        if db_name != 'ALX_prodev':
            print("Not connected to ALX_prodev database")
            return False
        
        # Check table exists and has correct structure
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_KEY 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'ALX_prodev' AND TABLE_NAME = 'user_data'
            ORDER BY ORDINAL_POSITION
        """)
        
        columns = cursor.fetchall()
        expected_columns = [
            ('user_id', 'varchar', 'NO', 'PRI'),
            ('name', 'varchar', 'NO', ''),
            ('email', 'varchar', 'NO', ''),
            ('age', 'decimal', 'NO', '')
        ]
        
        if len(columns) != len(expected_columns):
            print("Table structure mismatch")
            return False
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"Database validation error: {e}")
        return False


if __name__ == "__main__":
    """
    Main execution block for testing the functions.
    """
    print("Starting database setup...")
    
    # Step 1: Connect to MySQL server
    connection = connect_db()
    if not connection:
        print("Failed to connect to MySQL server")
        exit(1)
    
    # Step 2: Create database
    create_database(connection)
    connection.close()
    
    # Step 3: Connect to ALX_prodev database
    connection = connect_to_prodev()
    if not connection:
        print("Failed to connect to ALX_prodev database")
        exit(1)
    
    # Step 4: Create table
    create_table(connection)
    
    # Step 5: Insert data from CSV
    insert_data(connection, 'user_data.csv')
    
    # Step 6: Validate setup
    if validate_database_setup():
        print("Database setup completed successfully!")
    else:
        print("Database setup validation failed!")
    
    connection.close()
