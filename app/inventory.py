# app/inventory.py
# SmartFlow AI - Inventory + low stock alerts

class Inventory:
    def __init__(self):
        self.items = {}  # name -> {qty, cost, price, low_stock_at}

    def add_item(self, name: str, qty: int, cost: float, price: float, low_stock_at: int = 5):
        self.items[name.lower()] = {
            "name": name,
            "qty": qty,
            "cost": cost,
            "price": price,
            "low_stock_at": low_stock_at
        }

    def sell(self, name: str, qty: int):
        key = name.lower()
        if key not in self.items:
            return False, "Item not found"
        if self.items[key]["qty"] < qty:
            return False, "Not enough stock"
        self.items[key]["qty"] -= qty
        return True, f"Sold {qty} x {name}"

    def restock(self, name: str, qty: int):
        key = name.lower()
        if key in self.items:
            self.items[key]["qty"] += qty
            return True
        return False

    def low_stock(self):
        """Return list of items at or below low-stock level."""
        return [item for item in self.items.values() if item["qty"] <= item["low_stock_at"]]

    def stock_value(self) -> float:
        """Total value of stock at cost price."""
        return round(sum(item["qty"] * item["cost"] for item in self.items.values()), 2)

    def potential_profit(self) -> float:
        """Profit if all stock sells."""
        return round(sum(item["qty"] * (item["price"] - item["cost"]) for item in self.items.values()), 2)
