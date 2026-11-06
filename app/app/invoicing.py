# app/invoicing.py
"""Professional invoicing - VAT, due dates, WhatsApp-ready text."""
import uuid
from datetime import datetime, timedelta

def create_invoice(customer: str, items: list, vat_rate: float = 0.15):
    if not customer or not items:
        raise ValueError("Customer and at least one item required")
    subtotal = sum(i["qty"] * i["price"] for i in items)
    vat = round(subtotal * vat_rate, 2)
    total = round(subtotal + vat, 2)
    now = datetime.now()
    return {
        "id": f"INV-{uuid.uuid4().hex[:8].upper()}",
        "customer": customer,
        "items": items,
        "subtotal": subtotal,
        "vat": vat,
        "total": total,
        "date": now.strftime("%Y-%m-%d"),
        "due_date": (now + timedelta(days=7)).strftime("%Y-%m-%d"),
        "status": "unpaid",
    }

def invoice_text(inv: dict) -> str:
    lines = [f"INVOICE {inv['id']}", f"To: {inv['customer']}", f"Date: {inv['date']} | Due: {inv['due_date']}", "-" * 30]
    for i in inv["items"]:
        lines.append(f"{i['name']} x{i['qty']} @ R{i['price']:.2f} = R{i['qty']*i['price']:.2f}")
    lines += ["-" * 30, f"Subtotal: R{inv['subtotal']:.2f}", f"VAT (15%): R{inv['vat']:.2f}", f"TOTAL DUE: R{inv['total']:.2f}", f"Status: {inv['status'].upper()}", "Thank you for your business! - SmartFlow AI"]
    return "\n".join(lines)
