# app/invoicing.py
# SmartFlow AI - Invoicing module

from datetime import datetime, timedelta
import uuid

def create_invoice(customer_name: str, items: list, vat_rate: float = 0.0):
    """
    items = [{"name": "Airtime", "qty": 2, "price": 50}]
    Returns invoice dict with totals.
    """
    subtotal = sum(item["qty"] * item["price"] for item in items)
    vat = round(subtotal * vat_rate, 2)
    total = round(subtotal + vat, 2)

    invoice = {
        "invoice_id": f"INV-{str(uuid.uuid4())[:8].upper()}",
        "customer": customer_name,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "items": items,
        "subtotal": round(subtotal, 2),
        "vat": vat,
        "total": total,
        "status": "unpaid"
    }
    return invoice

def mark_paid(invoice: dict):
    invoice["status"] = "paid"
    invoice["paid_date"] = datetime.now().strftime("%Y-%m-%d")
    return invoice

def invoice_text(invoice: dict) -> str:
    """Simple text version for WhatsApp / printing."""
    lines = [
        f"INVOICE: {invoice['invoice_id']}",
        f"Customer: {invoice['customer']}",
        f"Date: {invoice['date']} | Due: {invoice['due_date']}",
        "------------------------------"
    ]
    for item in invoice["items"]:
        lines.append(f"{item['name']} x{item['qty']} @ R{item['price']} = R{item['qty'] * item['price']}")
    lines.append("------------------------------")
    lines.append(f"Subtotal: R{invoice['subtotal']}")
    lines.append(f"VAT: R{invoice['vat']}")
    lines.append(f"TOTAL: R{invoice['total']}")
    lines.append(f"Status: {invoice['status'].upper()}")
    return "\n".join(lines)
