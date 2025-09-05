# Python Generators - SQL Streaming Example

## Project Overview

This project demonstrates how to use Python to interact with a MySQL database, including creating a database and table, inserting data from a CSV file, and streaming rows one by one using a generator.

The goal is to efficiently handle database records without loading all data into memory at once, leveraging Python generators for streaming.

---

## Files

- `seed.py` - Contains functions to:
  - Connect to the MySQL server
  - Create the `ALX_prodev` database
  - Create the `user_data` table
  - Insert data from `user_data.csv`
  - Stream rows one by one using a generator

- `0-main.py` - Example usage script that:
  - Connects to the database
  - Creates the database and table
  - Inserts sample data
  - Demonstrates fetching rows

- `user_data.csv` - CSV file containing sample data to populate the database.

---

## Database Schema

**Database:** `ALX_prodev`  

**Table:** `user_data`

| Column   | Type         | Constraints                   |
|----------|-------------|--------------------------------|
| user_id  | CHAR(36)    | PRIMARY KEY, INDEXED           |
| name     | VARCHAR(255)| NOT NULL                       |
| email    | VARCHAR(255)| NOT NULL                       |
| age      | DECIMAL     | NOT NULL                       |

---

## Usage

1. Make sure MySQL server is running and accessible.
2. Ensure Python 3 and `mysql-connector-python` are installed:

```bash
pip install mysql-connector-python

