import asyncio
import aiosqlite

async def async_fetch_users():
    """Fetch all users from the database"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users') as cursor:
            users = await cursor.fetchall()
            print(f"All users: {len(users)} records found")
            return users

async def async_fetch_older_users():
    """Fetch users older than 40 from the database"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users WHERE age > 40') as cursor:
            older_users = await cursor.fetchall()
            print(f"Users older than 40: {len(older_users)} records found")
            return older_users

async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather"""
    print("Starting concurrent database queries...")
    
    # Execute both queries concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    print("Both queries completed!")
    return all_users, older_users