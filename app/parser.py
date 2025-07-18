# === parser.py ===
import re
from datetime import datetime
from dateparser.search import search_dates

def parse_invoice_command(command: str) -> dict:
    result = {
        "amount": None,
        "category": None,
        "invoice_date": None,
        "invoice_number": None,
        "description": None,
        "vendor": None,
        "taxes": {},
    }

    # Amount
    amount_match = re.search(r"\$?([\d,]+\.\d{2}|\d+)", command)
    if amount_match:
        result["amount"] = float(amount_match.group(1).replace(",", ""))

    # Category inference
    if "lease" in command.lower() and "truck" in command.lower():
        result["category"] = "Truck lease payment"
    elif "lease" in command.lower():
        result["category"] = "Lease Expense"
    elif "rent" in command.lower():
        result["category"] = "Rent Expense"
    elif "software" in command.lower():
        result["category"] = "Software"
    elif "consulting" in command.lower():
        result["category"] = "Consulting Expense"
    else:
        result["category"] = "General Expense"

    # Taxes (GST, PST, HST, QST)
    tax_types = ["GST", "PST", "HST", "QST"]
    for tax in tax_types:
        tax_match = re.search(rf"\$([\d\.]+)\s*{tax}", command, re.IGNORECASE)
        if tax_match:
            result["taxes"][tax] = float(tax_match.group(1))

    # Invoice number
    invoice_number_match = re.search(r"invoice number is (\d+)", command, re.IGNORECASE)
    if invoice_number_match:
        result["invoice_number"] = invoice_number_match.group(1)

    # Invoice date
    parsed_dates = search_dates(command)
    if parsed_dates:
        result["invoice_date"] = parsed_dates[0][1].date().isoformat()
    else:
        result["invoice_date"] = datetime.today().date().isoformat()

    # Vendor (fallback: first word after 'from' or use category keyword)
    from_match = re.search(r"from ([A-Za-z0-9 &]+)", command, re.IGNORECASE)
    if from_match:
        result["vendor"] = from_match.group(1).strip()
    elif result["category"]:
        result["vendor"] = result["category"].split()[0]
    else:
        result["vendor"] = "Unknown"

    # Description summary
    result["description"] = f"{result['category']}"

    return result
