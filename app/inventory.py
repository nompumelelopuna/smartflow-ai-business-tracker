# app/inventory.py
"""Inventory management - stock, low-stock alerts, profit."""
class Inventory:
    def __init__(self):
        self.items = {}
    def add_item(self, name: str, qty: int, cost: float, price: float, low_at: int = 5):
        self.items[name] = {"qty": qty, "cost": cost, "price": price, "low_at": low_at}
    def sell(self, name: str, qty: int):
        if name not in self.items:
            raise ValueError(f"{name} not in inventory")
        if self.items[name]["qty"] < qty:
            raise ValueError(f"Not enough {name} in stock")
        self.items[name]["qty"] -= qty
        return self.items[name]["qty"]
    def restock(self, name: str, qty: int):
        if name in self.items:
            self.items[name]["qty"] += qty
    def low_stock(self):
        return {k: v for k, v in self.items.items() if v["qty"] <= v["low_at"]}
    def stock_value(self):
        return sum(v["qty"] * v["cost"] for v in self.items.values())
    def potential_profit(self):
        return sum(v["qty"] * (v["price"] - v["cost"]) for v in self.items.values())
