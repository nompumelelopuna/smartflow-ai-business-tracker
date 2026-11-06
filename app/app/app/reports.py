# app/reports.py
"""Monthly reports + SARS-ready CSV export."""
import csv
from collections import defaultdict

def monthly_summary(transactions: list):
    income = sum(t[2] for t in transactions if t[4] == "income")
    expenses = sum(abs(t[2]) for t in transactions if t[4] == "expense")
    by_cat = defaultdict(float)
    for t in transactions:
        by_cat[t[3]] += t[2]
    return {"income": income, "expenses": expenses, "profit": income - expenses, "by_category": dict(by_cat), "count": len(transactions)}

def report_text(summary: dict) -> str:
    lines = ["SmartFlow AI - Monthly Report", f"Income: R{summary['income']:,.2f}", f"Expenses: R{summary['expenses']:,.2f}", f"Profit: R{summary['profit']:,.2f}", f"Transactions: {summary['count']}", "", "By Category:"]
    for k, v in summary["by_category"].items():
        lines.append(f"  {k}: R{v:,.2f}")
    return "\n".join(lines)

def export_csv(transactions: list, path: str = "sars_export.csv"):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Date", "Description", "Category", "Type", "Amount"])
        for t in transactions:
            w.writerow([t[5], t[1], t[3], t[4], t[2]])
    return path
