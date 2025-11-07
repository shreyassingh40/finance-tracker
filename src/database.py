# database.py
# -------------------------------------------------------
# This file handles everything related to the database.
# It creates a SQLite database, defines the table, and
# provides functions to insert and fetch transactions.
# -------------------------------------------------------

import sqlite3
from pathlib import Path

# Define the path to your database file inside the 'data' folder.
DB_PATH = Path("data/finance.db")

def connect_db():
    """
    Connect to the SQLite database (creates it if it doesn't exist).
    Returns a connection object.
    """
    # Ensure the data folder exists (in case user deleted it)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Connect to the database file
    return sqlite3.connect(DB_PATH)

def create_table():
    """
    Creates a table called 'transactions' if it doesn't already exist.
    Columns:
    - id: unique ID
    - date: transaction date
    - category: e.g. 'Food', 'Rent'
    - type: 'income' or 'expense'
    - amount: numeric value
    - description: optional note
    """
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            type TEXT CHECK(type IN ('expense','income')) NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
        """)
        conn.commit()

def insert_transaction(date, category, type, amount, description):
    """
    Inserts a new transaction into the database.
    Example: insert_transaction("2025-11-07", "Food", "expense", 12.5, "Lunch")
    """
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transactions (date, category, type, amount, description)
            VALUES (?, ?, ?, ?, ?)
        """, (date, category, type, amount, description))
        conn.commit()

def fetch_transactions():
    """
    Fetches all transactions as a list of tuples.
    Each tuple: (id, date, category, type, amount, description)
    """
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, date, category, type, amount, description
            FROM transactions
            ORDER BY date ASC
        """)
        return cur.fetchall()
