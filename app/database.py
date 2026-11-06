# app/database.py
# SmartFlow AI - SQLite database + transactions

import sqlite3
import os
from datetime import datetime

DB_PATH = "data/smartflow.db"

def get_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT DEFAULT 'other',
            type TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_transaction(description: str, amount: float, category: str, type: str):
    """type = 'income' or 'expense'. Amount positive for income."""
    conn = get_db()
    conn.execute(
        "INSERT INTO transactions (description, amount, category, type, date) VALUES (?, ?, ?, ?, ?)",
        (description, amount, category, type, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_transactions(limit: int = 100):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM transactions ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_totals():
    conn = get_db()
    row = conn.execute("""
        SELECT
        COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) as income,
        COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) as expenses
        FROM transactions
    """).fetchone()
    conn.close()
    income = row["income"]
    expenses = row["expenses"]
    return {
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "profit": round(income - expenses, 2)
    }
