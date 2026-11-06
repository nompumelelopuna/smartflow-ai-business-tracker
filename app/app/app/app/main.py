# app/main.py
# SmartFlow AI - Dashboard UI
# Run with: streamlit run app/main.py

import streamlit as st
from ai_engine import categorize, profit_summary
from database import init_db, add_transaction, get_transactions, get_totals
from invoicing import create_invoice, invoice_text
from inventory import Inventory
from customers import CustomerManager
from reports import monthly_summary, report_text

st.set_page_config(page_title="SmartFlow AI", page_icon="💰", layout="wide")
init_db()

st.title("💰 SmartFlow AI — Township Business OS")
st.caption("Money • Stock • Invoices • Customers • Tax — in one place. Built with Claude AI.")

# --- Dashboard ---
totals = get_totals()
col1, col2, col3 = st.columns(3)
col1.metric("Income", f"R{totals['income']}")
col2.metric("Expenses", f"R{totals['expenses']}")
col3.metric("Profit", f"R{totals['profit']}")

st.divider()

# --- Add Transaction ---
st.subheader("➕ Add Transaction")
with st.form("add_txn"):
    desc = st.text_input("Description (e.g. Sold airtime, Bought stock at Boxer)")
    amount = st.number_input("Amount (use - for expense, e.g. -500)", value=0.0)
    txn_type = st.selectbox("Type", ["income", "expense"])
    submitted = st.form_submit_button("Add")
    if submitted and desc:
        cat = categorize(desc)
        add_transaction(desc, abs(amount) if txn_type == "income" else -abs(amount), cat, txn_type)
        st.success(f"Added! AI category: {cat}")

# --- Recent Transactions ---
st.subheader("📋 Recent Transactions")
txns = get_transactions(20)
if txns:
    st.dataframe(txns, use_container_width=True)
    summary = monthly_summary(txns)
    st.text(report_text(summary))
else:
    st.info("No transactions yet. Add your first one above.")

st.divider()
st.caption("SmartFlow AI v2 • Built by Nompumelelo with Claude AI • Soweto")
