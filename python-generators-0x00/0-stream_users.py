#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.
    
    Yields:
        dict: A dictionary containing user data (user_id, name, email, age)
    """
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='ALX_prodev',
            user='your_username',
            password='your_password'
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Returns rows as dictionaries
            
            # Execute the query to fetch all users
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            
            # Single loop to fetch and yield rows one by one
            for row in cursor:
                yield row  # Yield the dictionary row
                
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        
    finally:
        # Clean up resources
        if connection.is_connected():
            cursor.close()
            connection.close()