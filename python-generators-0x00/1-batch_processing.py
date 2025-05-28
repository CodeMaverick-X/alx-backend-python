#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator function that streams rows from the user_data table in batches.
    
    Args:
        batch_size (int): Number of rows to fetch in each batch
        
    Yields:
        list: A list of dictionaries containing user data for each batch
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
            cursor = connection.cursor(dictionary=True)
            
            # Execute the query to fetch all users
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            
            # Loop 1: Fetch rows in batches
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
                
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        
    finally:
        # Clean up resources
        if connection.is_connected():
            cursor.close()
            connection.close()

def batch_processing(batch_size):
    """
    Process batches of users and filter those over the age of 25.
    
    Args:
        batch_size (int): Number of rows to process in each batch
    """
    # Loop 2: Process each batch from the generator
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: Filter users in each batch who are over 25
        for user in batch:
            if user['age'] > 25:
                print(user)