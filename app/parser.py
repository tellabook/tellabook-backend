from datetime import date
import re
from dateparser import parse as parse_date


def parse_invoice(text):
    vendor = None
    amount = None
    category = None
    invoice_date = None
    invoice_number = None
    description = ""

    # Extract amount
    amount_match = re.search(r"\$([\d,]+\.\d{2})", text)
    if amount_match:
        amount = float(amount_match.group(1).replace(",", ""))

    # Extract invoice number
    invoice_number_match = re.search(r"(invoice\s*#?\s*|number\s*:?)[#\s]*(\d+)", text, re.IGNORECASE)
    if invoice_number_match:
        invoice_number = invoice_number_match.group(2)

    # Extract date
    date_match = parse_date(text, settings={'PREFER_DATES_FROM': 'past'})
    invoice_date = date_match.date() if date_match else date.today()

    # Guess category
    if "lease" in text.lower() or "rent" in text.lower():
        category = "Lease Expense"
    elif "fuel" in text.lower():
        category = "Fuel"
    elif "repair" in text.lower() or "maintenance" in text.lower():
        category = "Repairs and Maintenance"

    # Vendor name guess (simple heuristic for now)
    vendor_match = re.search(r"from\s+([\w\s&]+)", text, re.IGNORECASE)
    if vendor_match:
        vendor = vendor_match.group(1).strip()

    # Default description as a summary
    description = f"Record {amount if amount else 'unknown'} expense from {vendor or 'unknown vendor'} on {invoice_date}"

    return {
        "vendor": vendor,
        "amount": amount,
        "category": category,
        "invoice_date": invoice_date,
        "invoice_number": invoice_number,
        "description": description
    }
