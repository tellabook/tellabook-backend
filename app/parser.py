import re
from datetime import datetime, date
from dateparser import parse as parse_date

def extract_amount(text):
    match = re.search(r"\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+)", text)
    if match:
        return float(match.group(1).replace(",", ""))
    return None

def extract_vendor(text):
    # Very basic logic to grab the word after "for"
    match = re.search(r"\bfor\s+([A-Za-z0-9&.\- ]+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip().split()[0]  # Just vendor name
    return "Unknown"

def extract_category(text):
    categories = {
        "internet": "Internet",
        "telus": "Internet",
        "rogers": "Internet",
        "lease": "Lease/Rent",
        "rent": "Lease/Rent",
        "payroll": "Payroll",
        "salary": "Payroll",
        "equipment": "Equipment",
        "truck": "Equipment",
        "repairs": "Repairs & Maintenance",
        "fuel": "Fuel",
        "insurance": "Insurance",
        "legal": "Legal Fees",
        "accounting": "Accounting Fees",
        "advertising": "Advertising"
    }
    text_lower = text.lower()
    for keyword, category in categories.items():
        if keyword in text_lower:
            return category
    return "Uncategorized"

def extract_date(text):
    dt = parse_date(text, settings={
        "PREFER_DATES_FROM": "past",
        "RELATIVE_BASE": datetime.now()
    })
    if isinstance(dt, datetime):
        return dt.date().isoformat()
    elif isinstance(dt, date):
        return dt.isoformat()
    return None

def parse_invoice_command(text):
    return {
        "amount": extract_amount(text),
        "vendor": extract_vendor(text),
        "category": extract_category(text),
        "invoice_date": extract_date(text),
        "description": text,
        "status": "staged"
    }
