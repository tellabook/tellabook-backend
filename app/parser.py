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
    terms = None
    tags = []
    memo = None
    fixed_asset_account = None
    inventory_account = None

    # Amount
    amount_match = re.search(r"\$([\d,]+\.\d{2})", text)
    if amount_match:
        amount = float(amount_match.group(1).replace(",", ""))

    # Invoice number
    invoice_number_match = re.search(r"(invoice\s*(?:number)?\s*[#:]?\s*)(\d+)", text, re.IGNORECASE)
    if invoice_number_match:
        invoice_number = invoice_number_match.group(2)

    # Date
    date_match = parse_date(text, settings={'PREFER_DATES_FROM': 'past'})
    invoice_date = date_match.date() if date_match else date.today()

    # Terms
    terms_match = re.search(r"(Net\s*\d+|Due on Receipt)", text, re.IGNORECASE)
    if terms_match:
        terms = terms_match.group(1)

    # Tags (looking for phrases like "tagged to XYZ")
    tag_match = re.findall(r"tagged to ([\w\s,&]+)", text, re.IGNORECASE)
    if tag_match:
        tags = [tag.strip() for tag in tag_match]

    # Memo (looking for “note:” or “memo:”)
    memo_match = re.search(r"(?:note|memo)[:\-]\s*(.+)", text, re.IGNORECASE)
    if memo_match:
        memo = memo_match.group(1).strip()

    # Asset or inventory account
    if "fixed asset" in text.lower():
        fixed_asset_account = "Fixed Asset"
    if "inventory" in text.lower():
        inventory_account = "Inventory"

    # Category
    lowered = text.lower()
    if "lease" in lowered or "rent" in lowered:
        category = "Lease Expense"
    elif "fuel" in lowered:
        category = "Fuel"
    elif "repair" in lowered or "maintenance" in lowered:
        category = "Repairs and Maintenance"
    else:
        category = "General Expense"

    # Vendor
    vendor_match = re.search(r"from\s+([a-zA-Z0-9 &]+)", text, re.IGNORECASE)
    if vendor_match:
        vendor = vendor_match.group(1).strip()

    # Description
    description = f"{category} of ${amount if amount else 'unknown'} from {vendor or 'unknown vendor'} on {invoice_date}"

    return {
        "vendor": vendor,
        "amount": amount,
        "category": category,
        "invoice_date": invoice_date,
        "invoice_number": invoice_number,
        "terms": terms,
        "tags": ", ".join(tags) if tags else None,
        "memo": memo,
        "fixed_asset_account": fixed_asset_account,
        "inventory_account": inventory_account,
        "description": description
    }
