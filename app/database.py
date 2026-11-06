# app/database.py
"""SQLite persistence for SmartFlow AI - offline-first."""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "smartflow.db")

def _connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    with _connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT DEFAULT 'other',
            type TEXT CHECK(type IN ('income','expense')) NOT NULL,
            date TEXT NOT NULL
        )""")

def add_transaction(description: str, amount: float, category: str = "other", txn_type: str = "income"):
    if not description or amount == 0:
        raise ValueError("Description required and amount cannot be 0")
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    with _connect() as conn:
        conn.execute("INSERT INTO transactions (description, amount, category, type, date) VALUES (?,?,?,?,?)",
                     (description, amount, category, txn_type, date))

def get_transactions(limit: int = 100):
    with _connect() as conn:
        return conn.execute("SELECT id, description, amount, category, type, date FROM transactions ORDER BY id DESC LIMIT ?", (limit,)).fetchall()

def get_totals():
    with _connect() as conn:
        rows = conn.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type").fetchall()
    d = dict(rows)
    income = d.get("income", 0) or 0
    expenses = abs(d.get("expense", 0) or 0)
    return {"income": income, "expenses": expenses, "profit": income - expenses}
