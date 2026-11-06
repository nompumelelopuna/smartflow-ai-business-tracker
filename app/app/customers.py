# app/customers.py
# SmartFlow AI - Customers + debt tracking

from datetime import datetime

class CustomerManager:
    def __init__(self):
        self.customers = {}  # name -> {phone, total_owed, history}

    def add_customer(self, name: str, phone: str = ""):
        if name.lower() not in self.customers:
            self.customers[name.lower()] = {
                "name": name,
                "phone": phone,
                "total_owed": 0.0,
                "history": []
            }
        return self.customers[name.lower()]

    def add_debt(self, name: str, amount: float, note: str = ""):
        customer = self.add_customer(name)
        customer["total_owed"] = round(customer["total_owed"] + amount, 2)
        customer["history"].append({
            "type": "debt",
            "amount": amount,
            "note": note,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        return customer

    def record_payment(self, name: str, amount: float):
        customer = self.add_customer(name)
        customer["total_owed"] = round(max(0, customer["total_owed"] - amount), 2)
        customer["history"].append({
            "type": "payment",
            "amount": amount,
            "note": "Payment received",
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        return customer

    def who_owes_me(self):
        """Return customers who still owe money, highest first."""
        debtors = [c for c in self.customers.values() if c["total_owed"] > 0]
        return sorted(debtors, key=lambda x: x["total_owed"], reverse=True)

    def total_debt(self) -> float:
        return round(sum(c["total_owed"] for c in self.customers.values()), 2)
