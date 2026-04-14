# database.py
# --------------------------------------------------------
# Database functions for Personal Finance Tracker
# --------------------------------------------------------

import sqlite3
from pathlib import Path

DB_PATH = Path("data/finance.db")

def connect_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_table():
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            type TEXT CHECK(type IN ('expense','income')) NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
        """)
        conn.commit()

def insert_transaction(username, date, category, type, amount, description):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO transactions (username, date, category, type, amount, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (username, date, category.strip().title(), type, float(amount), description.strip()),
        )
        conn.commit()

def fetch_transactions(username):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, username, date, category, type, amount, description
            FROM transactions
            WHERE username = ?
            ORDER BY date ASC, id ASC
        """, (username,))
        return cur.fetchall()