#!/usr/bin/python3
import mysql.connector

# Connect to ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # replace with your MySQL password if any
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Generator to fetch users in batches
def stream_users_in_batches(batch_size):
    connection = connect_to_prodev()
    if connection is None:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    
    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    # Yield any remaining rows
    if batch:
        yield batch

    cursor.close()
    connection.close()

# Process each batch to filter users over the age of 25
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
