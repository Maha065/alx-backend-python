from datetime import datetime
import sqlite3
import functools

#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Handle both positional and keyword query arguments
        if args:
            print(f"[LOG] Executing SQL Query: {args[0]}")
        elif "query" in kwargs:
            print(f"[LOG] Executing SQL Query: {kwargs['query']}")
        else:
            print("[LOG] No SQL Query provided")
        
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
