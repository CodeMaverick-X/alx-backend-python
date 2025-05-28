#!/usr/bin/python3
import seed

def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database.
    
    Args:
        page_size (int): Number of users to fetch per page
        offset (int): Number of records to skip
        
    Returns:
        list: List of user dictionaries for the requested page
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """
    Generator function that lazily fetches paginated data from the users database.
    Only fetches the next page when needed.
    
    Args:
        page_size (int): Number of users to fetch per page
        
    Yields:
        list: A list of user dictionaries for each page
    """
    offset = 0
    
    # Single loop to fetch pages lazily
    while True:
        page = paginate_users(page_size, offset)
        
        # If no more data, stop the generator
        if not page:
            break
            
        yield page
        offset += page_size

# Alias for the test script
lazy_pagination = lazy_paginate