# app/ai_engine.py
# SmartFlow AI - AI auto-categorization engine

CATEGORIES = {
    "stock": ["stock", "inventory", "buy", "supplier", "wholesale", "boxer", "makro"],
    "transport": ["taxi", "petrol", "fuel", "uber", "bolt", "transport"],
    "food": ["food", "lunch", "groceries", "bread", "milk"],
    "sales": ["sale", "sold", "payment", "customer paid", "invoice paid"],
    "airtime": ["airtime", "data", "vodacom", "mtn", "telkom"],
    "rent": ["rent", "shop rent", "stall"],
}

def categorize(description: str) -> str:
    """Auto-categorize a transaction from its description."""
    text = description.lower()
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in text:
                return category
    return "other"

def suggest_price(cost: float, margin: float = 0.3) -> float:
    """Suggest selling price from cost + margin."""
    return round(cost * (1 + margin), 2)

def profit_summary(transactions: list) -> dict:
    """Calculate total income, expenses, profit."""
    income = sum(t["amount"] for t in transactions if t["amount"] > 0)
    expenses = sum(abs(t["amount"]) for t in transactions if t["amount"] < 0)
    return {
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "profit": round(income - expenses, 2)
    }
