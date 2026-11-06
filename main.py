# app/main.py
# SmartFlow AI - Professional Dashboard
# Run: streamlit run app/main.py

import streamlit as st
import pandas as pd

try:
    from app.ai_engine import categorize
    from app.database import init_db, add_transaction, get_transactions, get_totals
    from app.invoicing import create_invoice, invoice_text
    from app.inventory import Inventory
    from app.customers import CustomerManager
    from app.reports import monthly_summary, report_text
except ImportError:
    from ai_engine import categorize
    from database import init_db, add_transaction, get_transactions, get_totals
    from invoicing import create_invoice, invoice_text
    from inventory import Inventory
    from customers import CustomerManager
    from reports import monthly_summary, report_text

st.set_page_config(page_title="SmartFlow AI | Township Business OS", page_icon="💰", layout="wide")

# --- Professional Styling ---
st.markdown("""
<style>
.main { background-color: #F8F9FA; }
div[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #E9ECEF;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.stButton > button {
    background-color: #0F5132;
    color: white;
    border-radius: 8px;
    font-weight: 600;
    border: none;
    padding: 8px 20px;
}
.stButton > button:hover { background-color: #146C43; color: white; }
h1, h2, h3 { color: #0F5132; }
</style>
""", unsafe_allow_html=True)

init_db()

# --- Sidebar ---
with st.sidebar:
    st.title("💰 SmartFlow AI")
    st.caption("Township Business OS")
    st.divider()
    page = st.radio("Navigate", ["📊 Dashboard", "➕ Add Transaction", "🧾 Create Invoice", "📦 Inventory", "👥 Customers"])
    st.divider()
    st.caption("Built with Claude Code")
    st.caption("For Alignerr Evaluation")
    st.caption("Soweto, South Africa")

# --- Header ---
st.title("SmartFlow AI — Township Business OS")
st.caption("Money • Stock • Invoices • Customers • Tax — in one place. Built for Soweto hustlers.")

totals = get_totals()
c1, c2, c3, c4 = st.columns(4)
c1.metric("💵 Total Income", f"R {totals['income']:,.2f}")
c2.metric("💸 Total Expenses", f"R {totals['expenses']:,.2f}")
c3.metric("📈 Net Profit", f"R {totals['profit']:,.2f}", delta=f"R {totals['profit']:,.2f}")
profit_margin = (totals['profit'] / totals['income'] * 100) if totals['income'] > 0 else 0
c4.metric("📊 Profit Margin", f"{profit_margin:.1f}%")

st.divider()

if page == "📊 Dashboard":
    st.subheader("📋 Recent Transactions")
    txns = get_transactions(20)
    if txns:
        df = pd.DataFrame(txns, columns=["ID", "Description", "Amount", "Category", "Type", "Date"])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.subheader("📊 Monthly Report")
        summary = monthly_summary(txns)
        st.code(report_text(summary), language="text")
        st.download_button("⬇️ Download SARS CSV", data=df.to_csv(index=False), file_name="sars_export.csv", mime="text/csv")
    else:
        st.info("👋 Welcome to SmartFlow AI! No transactions yet. Go to Add Transaction to log your first sale.")
        st.markdown("**Try this:** Sold airtime R200 | Bought stock at Boxer -R1500")

elif page == "➕ Add Transaction":
    st.subheader("➕ Add New Transaction")
    st.info("Type in plain language — AI will categorize it for you.")
    with st.form("add_txn", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        desc = col_a.text_input("Description", placeholder="e.g. Sold airtime, Bought stock at Boxer")
        amount = col_b.number_input("Amount (R)", value=0.0, step=10.0)
        txn_type = st.selectbox("Type", ["income", "expense"])
        submitted = st.form_submit_button("✅ Add Transaction", use_container_width=True)
        if submitted:
            if not desc:
                st.error("Please enter a description.")
            elif amount == 0:
                st.error("Amount cannot be 0.")
            else:
                cat = categorize(desc)
                final_amount = abs(amount) if txn_type == "income" else -abs(amount)
                add_transaction(desc, final_amount, cat, txn_type)
                st.success(f"Added! AI Category: **{cat}** | Amount: R {final_amount:,.2f}")
                st.balloons()

elif page == "🧾 Create Invoice":
    st.subheader("🧾 Create Professional Invoice")
    with st.form("invoice_form"):
        customer = st.text_input("Customer Name", placeholder="e.g. Thabo's Spaza")
        item = st.text_input("Item", placeholder="e.g. Airtime")
        qty = st.number_input("Quantity", min_value=1, value=1)
        price = st.number_input("Price per item (R)", min_value=0.0, value=50.0)
        submitted = st.form_submit_button("Generate Invoice", use_container_width=True)
        if submitted and customer and item:
            inv = create_invoice(customer, [{"name": item, "qty": qty, "price": price}], vat_rate=0.15)
            st.success(f"Invoice {inv['id']} created!")
            st.code(invoice_text(inv), language="text")
            st.caption("Copy the text above and send it via WhatsApp to your customer.")

elif page == "📦 Inventory":
    st.subheader("📦 Inventory Overview")
    st.info("Inventory module connected. Low-stock alerts help you never run out of best sellers.")
    inv = Inventory()
    st.caption("Demo stock: Add your real stock via code or dashboard in Phase 2.")

elif page == "👥 Customers":
    st.subheader("👥 Customers & Debt")
    st.info("Track who owes you. Add debt when they buy on credit, record payment when they pay.")
    cm = CustomerManager()
    st.caption("Use who_owes_me() to see your biggest debtors first.")

st.divider()
st.caption("SmartFlow AI v2.0 • Built by Nompumelelo with Claude Code • Soweto • MIT License")
