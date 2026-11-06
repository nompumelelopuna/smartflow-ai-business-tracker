# SmartFlow AI — Township Business OS

Built with Claude Code for Alignerr evaluation.
Demonstrates agentic development workflow: planning, atomic commits, modular Python architecture, and AI-assisted debugging.

Badges: Python 3.11+ | SQLite | Streamlit | Claude Code | Alignerr | MVP Complete

---

## Table of Contents
- Project Overview
- Why This Project
- Key Features
- Tech Stack
- Project Structure
- Getting Started
- How It Works
- Agentic Workflow — How It Was Built
- Build History
- Roadmap
- Author

---

## Project Overview

SmartFlow AI is a lightweight, offline-first Business OS for township businesses in Soweto, South Africa.

Spaza shops, vendors, and hustlers lose money not from lack of effort, but from lack of tracking — cash in/out in their head, customers buying on credit and never paying, stock running out without warning, and no records for SARS.

SmartFlow AI solves this in one app:
Money - Stock - Invoices - Customers - Tax

Built to work on a phone or low-end laptop, with no subscription, no spreadsheets, and no accountant needed.

---

## Why This Project

This project was chosen for Alignerr evaluation because it tests exactly what real-world agentic coding requires:

1. Real user problem — Not a todo-list clone. Solves a painful, specific problem.
2. Multiple interconnected modules — AI, DB, invoicing, inventory, customers, reports must all work together.
3. Plain-language input — AI must interpret messy human text like Sold airtime R200 or Bought stock at Boxer -R1500.
4. Edge cases — Negative amounts, missing stock, over-payment, VAT, CSV export.
5. Clean architecture — Each module is independent, testable, and reusable.

---

## Key Features

### 1. AI Transaction Categorization - ai_engine.py
Type in plain language, AI categorizes automatically:
- Sold airtime R200 = income / sales
- Bought stock at Boxer -R1500 = expense / stock
- Taxi to Joburg -R120 = expense / transport

Includes keyword-based classification, fallback to other, and profit summary aggregation.

### 2. Transactions + SQLite Database - database.py
- init_db() creates tables automatically
- add_transaction() / get_transactions() / get_totals()
- Persistent, offline-first storage — no server needed
- Full history with date, description, category, type, amount

### 3. Professional Invoicing - invoicing.py
- Auto-generated IDs: INV-XXXXXXXX
- VAT calculation, 7-day due dates, paid/unpaid status
- invoice_text() — WhatsApp-ready format, copy-paste to customer
- Designed for schools, churches, and local businesses who need formal invoices

### 4. Inventory + Low-Stock Alerts - inventory.py
- Track qty, cost price, selling price, low-stock threshold per item
- sell() with stock validation, restock() to add stock
- low_stock() returns items needing reorder
- stock_value() and potential_profit() for business insight

### 5. Customers + Debt Tracking - customers.py
- Customer profiles with phone + transaction history
- add_debt() when they buy on credit, record_payment() when they pay
- who_owes_me() — sorted by amount owed, highest first
- total_debt() — total outstanding across all customers

### 6. Monthly Reports + SARS Export - reports.py
- monthly_summary() — income, expenses, profit, breakdown by category
- report_text() — clean text report for WhatsApp / printing
- export_csv() — SARS-ready CSV (sars_export.csv) for accountant / tax filing

### 7. Streamlit Dashboard - main.py
- Metrics: Income / Expenses / Profit at a glance
- Add Transaction form with live AI categorization
- Recent Transactions table + Monthly Report view
- Mobile-friendly, runs on localhost:8501

---

## Tech Stack

Layer | Technology | Reason
--- | --- | ---
Language | Python 3.11+ | Readable, fast to prototype, ideal for MVP
Database | SQLite | Zero-config, offline-first, file-based
UI | Streamlit | Fast dashboard, works on phone + laptop
AI Logic | Rule-based AI Engine | Lightweight, no API cost, works offline
Version Control | Git + GitHub | Atomic commits, professional workflow
AI Partner | Claude Code | Agentic planning, codegen, debugging, docs

---

## Project Structure

SmartFlow-AI/
- README
- CLAUDE
- requirements
- app/
    - init file
    - ai_engine
    - database
    - invoicing
    - inventory
    - customers
    - reports
    - main
- data/
    - smartflow db

Design principle: Each module is independent and testable. You can import invoicing without inventory, or reports without the dashboard.

---

## Getting Started

Prerequisites
- Python 3.11+
- Git

1. Clone
git clone YOUR-REPO-LINK-HERE
cd SmartFlow-AI

2. Install
pip install -r requirements.txt

3. Run Dashboard
streamlit run app/main.py
Open localhost:8501

4. Quick Test (No UI)
from app.ai_engine import categorize
from app.database import init_db, add_transaction, get_totals
from app.invoicing import create_invoice, invoice_text

init_db()
add_transaction("Sold airtime", 200, categorize("Sold airtime"), "income")
add_transaction("Bought stock at Boxer", -1500, categorize("Bought stock"), "expense")

print(get_totals())
invoice = create_invoice("Thabo's Spaza", [{"name": "Airtime", "qty": 2, "price": 50}], vat_rate=0.15)
print(invoice_text(invoice))

---

## How It Works

1. User types plain language: Sold vetkoek R500
2. AI Engine scans keywords and assigns category: sales
3. Database saves with date, amount, category, type
4. Dashboard updates Income / Expenses / Profit instantly
5. Reports aggregates by month to CSV for SARS

---

## Agentic Workflow — How It Was Built

This project was built using Claude Code in an agentic workflow, not by copy-pasting code.

Workflow used:
1. Plan: Defined problem, user (Soweto spaza owner), and MVP scope with Claude
2. Scaffold: Created repo structure, CLAUDE file, and requirements file
3. Build in atomic commits: One feature per commit, each tested before moving on
4. Iterate: Used Claude to debug, refactor, and improve each module
5. Document: README written to explain why decisions were made, not just what code does

What this demonstrates for Alignerr:
- Ability to break a large task into small, verifiable steps
- Ability to give clear prompts and validate AI output
- Ability to maintain clean commit history and modular code
- Ability to document for a human reviewer, not just for the machine

Prompts used (examples):
- Create an AI engine that categorizes township transactions from plain language
- Add SQLite persistence with totals and history
- Make invoicing WhatsApp-ready for township customers
- Add low-stock alerts and profit calculation to inventory

---

## Build History

1 - init: project scaffold with README and CLAUDE - Repo setup, structure, AI instructions
2 - feat: add AI categorization engine - Keyword AI, profit summary
3 - feat: add transactions + SQLite DB - Database layer, totals, history
4 - feat: add invoicing module - Invoices, VAT, WhatsApp format
5 - feat: add inventory + low stock alerts - Stock mgmt, value + profit
6 - feat: add customers + debt tracking - Profiles, debt, payments
7 - feat: add monthly reports + SARS export - Monthly summary, CSV export
8 - feat: add dashboard UI + polish - Streamlit dashboard
9 - docs: Alignerr-ready README for Claude Code evaluation - This README

---

## Roadmap

Phase 1 — MVP Complete
- AI categorization, Transactions, Invoicing, Inventory, Customers, Reports, Dashboard

Phase 2 — Next
- WhatsApp Bot — auto-send invoice via WhatsApp
- Voice input — speak transaction, AI logs it
- PDF invoice generation
- Multi-business support

Phase 3 — Vision
- AI business coach: Profit dropped 20 percent because stock costs rose
- Stokvel / savings tracking
- Yoco / SnapScan / Capitec integration

---

## Author

Nompumelelo — Soweto, South Africa

Building real software with Claude Code. Learning agentic workflows, clean architecture, and shipping MVPs that solve real township problems.


---

## License

MIT License — free to use, learn from, and build on.

---

## Acknowledgements

- Built with Claude Code as agentic partner for planning, codegen, and documentation.
- Submitted for Alignerr evaluation.
- Inspired by the spaza shops, vendors, and hustlers of Soweto who keep the township economy alive.

If this helped you, star the repo and share it with a hustler who needs it..
