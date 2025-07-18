import re
from datetime import datetime
import dateparser

def parse_invoice_command(command: str) -> dict:
    # === Extract amount ===
    amount_match = re.search(r'\$?([\d,]+\.?\d*)', command)
    amount = float(amount_match.group(1).replace(',', '')) if amount_match else 0.0

    # === Extract vendor (guess: first proper noun after 'for') ===
    vendor_match = re.search(r'for ([\w\s&\-]+?)( from| on| as| starting| due|\,|\.)', command, re.IGNORECASE)
    vendor = vendor_match.group(1).strip() if vendor_match else "Unknown Vendor"

    # === Extract category based on keyword hints ===
    category = "General Expense"
    lower_command = command.lower()
    if "lease" in lower_command:
        category = "Lease Expense"
    elif "truck lease" in lower_command:
        category = "Truck Lease payment"
    elif "rent" in lower_command:
        category = "Rent"
    elif "software" in lower_command:
        category = "Software Subscription"
    elif "office" in lower_command:
        category = "Office Expense"

    # === Extract taxes ===
    taxes = {}
    tax_matches = re.findall(r'\$([\d\.]+)\s*(GST|PST|HST|QST)', command, re.IGNORECASE)
    for amount_str, tax_type in tax_matches:
        taxes[tax_type.upper()] = float(amount_str)

    # === Extract invoice number if present ===
    invoice_number_match = re.search(r'invoice number is (\d+)', command, re.IGNORECASE)
    invoice_number = invoice_number_match.group(1) if invoice_number_match else None

    # === Extract date from text ===
    parsed_date = dateparser.search.search_dates(command)
    invoice_date = None
    if parsed_date:
        invoice_date = parsed_date[0][1].date().isoformat()
    else:
        invoice_date = datetime.today().date().isoformat()  # fallback to today

    # === Description (summarized) ===
    description = f"{category}"

    return {
        "vendor": vendor,
        "amount": amount,
        "category": category,
        "invoice_date": invoice_date,
        "description": description,
        "taxes": taxes,
        "invoice_number": invoice_number
    }
