import sqlite3, os
from datetime import datetime

DB = "smartflow.db"

CATEGORIES = {
    "Transport": ["uber","taxi","bolt","petrol","fuel","courier","delivery"],
    "Stock": ["stock","inventory","supplier","wholesale","goods"],
    "Utilities": ["airtime","data","electricity","wifi","mtn","vodacom","telkom"],
    "Marketing": ["ads","facebook","boost","flyer"],
    "Food": ["lunch","groceries","shoprite"],
}

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS transactions 
    (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, type TEXT, category TEXT, amount REAL, description TEXT)''')
    conn.commit(); conn.close()

def ai_categorize(desc):
    d = desc.lower()
    for cat, kws in CATEGORIES.items():
        if any(k in d for k in kws):
            return cat
    return "Other" if "expense" in d else "Sales"

def add(t_type, amount, desc):
    init_db()
    cat = ai_categorize(desc)
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO transactions (date,type,category,amount,description) VALUES (?,?,?,?,?)",
                 (date, t_type, cat, amount, desc))
    conn.commit(); conn.close()
    print(f"✅ Added {t_type}: R{amount} | {cat} | {desc} [Auto-categorized by SmartFlow AI]")

def summary():
    init_db()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    income = cur.fetchone()[0] or 0
    cur.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    expense = cur.fetchone()[0] or 0
    cur.execute("SELECT category, SUM(amount) as total FROM transactions WHERE type='expense' GROUP BY category ORDER BY total DESC")
    top = cur.fetchall()
    conn.close()
    
    print("\n=== SmartFlow AI Business Insights ===")
    print(f"💰 Income: R{income:.2f} | 💸 Expense: R{expense:.2f} | 📈 Profit: R{income-expense:.2f}")
    if top:
        print(f"⚠️  Top Cost: {top[0][0]} - R{top[0][1]:.2f}")
        if top[0][1] > expense*0.4:
            print(f"🤖 AI INSIGHT: {top[0][0]} is {top[0][1]/expense*100:.0f}% of all expenses. Try to batch or negotiate this cost.")
    if income > 0 and (income-expense)/income > 0.3:
        print(f"🤖 AI INSIGHT: Healthy margin {((income-expense)/income*100):.0f}%. You can reinvest R{(income-expense)*0.2:.2f} into marketing.")
    print("======================================\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py add <income/expense> <amount> <description> OR python main.py summary")
    elif sys.argv[1] == "add":
        add(sys.argv[2], float(sys.argv[3]), " ".join(sys.argv[4:]))
    elif sys.argv[1] == "summary":
        summary()
    elif sys.argv[1] == "init":
        init_db(); print("DB initialized")
