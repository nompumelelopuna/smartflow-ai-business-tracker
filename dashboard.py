import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="SmartFlow AI", page_icon="🚀", layout="wide")

# --- CUSTOM CSS TO MATCH PHOTO ---
st.markdown("""
<style>
    .stApp { background-color: #0E0F14; color: white; }
    [data-testid="stSidebar"] { background-color: #0A0B10; }
    .metric-card {
        background: #1A1C24;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #2A2D3A;
    }
    .metric-title { color: #9CA3AF; font-size: 14px; }
    .metric-value { color: white; font-size: 42px; font-weight: bold; }
    .green-text { color: #4ADE80; font-size: 13px; }
    .red-text { color: #F87171; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

DB = "smartflow.db"

# --- HEADER ---
col_h1, col_h2 = st.columns([3,1])
with col_h1:
    st.markdown("# 🚀 SmartFlow AI")
    st.markdown("<p style='color:#9CA3AF; margin-top:-15px;'>Business Tracking Dashboard</p>", unsafe_allow_html=True)
with col_h2:
    st.markdown("<div style='text-align:right;'><span style='background:#1A1C24; padding:8px 16px; border-radius:20px; color:#4ADE80;'>● Live • Connected</span> <span style='background:#1A1C24; padding:8px 16px; border-radius:20px; margin-left:8px;'>Admin SF</span></div>", unsafe_allow_html=True)

# --- SIDEBAR MENU (Like photo) ---
with st.sidebar:
    st.markdown("<p style='color:#6B7280; font-size:12px; letter-spacing:2px;'>MENU</p>", unsafe_allow_html=True)
    menu = st.radio("", ["Dashboard", "Transactions", "Reports", "Analytics", "Settings", "Help & Support"], label_visibility="collapsed")
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.caption("Streamlit • v1.39 • Dark Theme")

# --- LOAD DATA ---
conn = sqlite3.connect(DB)
try:
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
except:
    df = pd.DataFrame()
conn.close()

if df.empty:
    # DEMO DATA if empty so it looks like photo
    df = pd.DataFrame([
        {"date":"2024-10-01", "category":"Stock", "description":"Inventory Restock", "amount":400, "type":"expense"},
        {"date":"2024-09-30", "category":"Transport", "description":"Fuel Purchase", "amount":200, "type":"expense"},
        {"date":"2024-09-29", "category":"Utilities", "description":"Electricity Bill", "amount":50, "type":"expense"},
        {"date":"2024-09-28", "category":"Income", "description":"Client Payment", "amount":1500, "type":"income"},
        {"date":"2024-09-27", "category":"Transport", "description":"Courier Fees", "amount":150, "type":"expense"},
    ])
    income = 2500
    expense = 800
    profit = 1700
else:
    income = df[df['type']=='income']['amount'].sum()
    expense = df[df['type']=='expense']['amount'].sum()
    profit = income-expense

# --- OVERVIEW SECTION ---
st.markdown("## Overview")
st.markdown("<p style='color:#9CA3AF;'>01 October 2024 • Today</p>", unsafe_allow_html=True)

# METRICS CARDS - 3 columns like photo
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-title'>↗ Total Income</div>
        <div class='metric-value'>R{income:.0f}</div>
        <div class='green-text'>+12% vs last month ↗</div>
    </div>
    """, unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-title'>↘ Total Expense</div>
        <div class='metric-value'>R{expense:.0f}</div>
        <div class='red-text'>+5% vs last month ↗</div>
    </div>
    """, unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-title'>◉ Profit</div>
        <div class='metric-value'>R{profit:.0f}</div>
        <div class='green-text'>+18% vs last month ↗</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# SECOND ROW
c1, c2 = st.columns([1, 1.5])

with c1:
    st.markdown("""
    <div class='metric-card'>
        <h3>Spending by Category</h3>
        <p style='color:#9CA3AF; text-align:right; margin-top:-35px;'>October 2024</p>
    </div>
    """, unsafe_allow_html=True)
    # Bar chart data
    chart_data = df[df['type']=='expense'].groupby("category")["amount"].sum() if not df.empty else pd.Series([350,400,50], index=["Transport","Stock","Utilities"])
    st.bar_chart(chart_data)

with c2:
    st.markdown("""
    <div class='metric-card'>
        <h3>Recent Transactions <span style='float:right; color:#4ADE80; font-size:14px;'>View All →</span></h3>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
