# app/customers.py
"""Customer & debt tracking - who owes you."""
class CustomerManager:
    def __init__(self):
        self.customers = {}
    def add_customer(self, name: str, phone: str = ""):
        if name not in self.customers:
            self.customers[name] = {"phone": phone, "debt": 0.0, "history": []}
    def add_debt(self, name: str, amount: float, note: str = ""):
        self.add_customer(name)
        self.customers[name]["debt"] += amount
        self.customers[name]["history"].append({"type": "debt", "amount": amount, "note": note})
    def record_payment(self, name: str, amount: float):
        if name not in self.customers:
            raise ValueError("Customer not found")
        self.customers[name]["debt"] = max(0, self.customers[name]["debt"] - amount)
        self.customers[name]["history"].append({"type": "payment", "amount": amount, "note": ""})
    def who_owes_me(self):
        return sorted([(k, v["debt"]) for k, v in self.customers.items() if v["debt"] > 0], key=lambda x: x[1], reverse=True)
    def total_debt(self):
        return sum(v["debt"] for v in self.customers.values())
