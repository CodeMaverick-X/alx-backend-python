#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    """
    Generator function that yields user ages one by one from the database.
    Memory-efficient as it processes one age at a time.
    
    Yields:
        int: Individual user age
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
            cursor = connection.cursor()
            
            # Execute query to fetch only ages
            cursor.execute("SELECT age FROM user_data")
            
            # Loop 1: Yield ages one by one
            for (age,) in cursor:
                yield age
                
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        
    finally:
        # Clean up resources
        if connection.is_connected():
            cursor.close()
            connection.close()

def calculate_average_age():
    """
    Calculate the average age of users without loading the entire dataset into memory.
    Uses the stream_user_ages generator for memory efficiency.
    
    Returns:
        float: Average age of all users
    """
    total_age = 0
    count = 0
    
    # Loop 2: Process ages one by one to calculate average
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0
    
    return total_age / count

# Calculate and print the average age
if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age}")