# app/reports.py
# SmartFlow AI - Monthly reports + SARS-ready export

import csv
from datetime import datetime
from collections import defaultdict

def monthly_summary(transactions: list, month: str = None):
    """
    month format: '2026-11' — if None, uses current month.
    transactions = list of dicts with amount, category, date
    """
    if month is None:
        month = datetime.now().strftime("%Y-%m")

    filtered = [t for t in transactions if t.get("date", "").startswith(month)]
    income = sum(t["amount"] for t in filtered if t["amount"] > 0)
    expenses = sum(abs(t["amount"]) for t in filtered if t["amount"] < 0)

    by_category = defaultdict(float)
    for t in filtered:
        by_category[t.get("category", "other")] += t["amount"]

    return {
        "month": month,
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "profit": round(income - expenses, 2),
        "transaction_count": len(filtered),
        "by_category": dict(by_category)
    }

def export_csv(transactions: list, filename: str = "data/sars_export.csv"):
    """Export transactions to CSV for SARS / accountant."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "description", "category", "type", "amount"])
        writer.writeheader()
        for t in transactions:
            writer.writerow({
                "date": t.get("date", ""),
                "description": t.get("description", ""),
                "category": t.get("category", ""),
                "type": t.get("type", ""),
                "amount": t.get("amount", 0)
            })
    return filename

def report_text(summary: dict) -> str:
    """Pretty text report for WhatsApp / printing."""
    lines = [
        f"SmartFlow AI — Monthly Report: {summary['month']}",
        "------------------------------",
        f"Income: R{summary['income']}",
        f"Expenses: R{summary['expenses']}",
        f"Profit: R{summary['profit']}",
        f"Transactions: {summary['transaction_count']}",
        "------------------------------",
        "By Category:"
    ]
    for cat, total in summary["by_category"].items():
        lines.append(f"  {cat}: R{round(total, 2)}")
    return "\n".join(lines)
