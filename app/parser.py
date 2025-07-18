import re
from dateparser import parse as parse_date
from datetime import datetime

# Define keyword to category mapping
CATEGORY_KEYWORDS = {
    "lease": "Lease Expense",
    "rent": "Rent",
    "internet": "Internet",
    "phone": "Telecom",
    "telus": "Telecom",
    "rogers": "Telecom",
    "office": "Office Supplies",
    "printer": "Office Supplies",
    "utilities": "Utilities"
}

# Default tax rates by province
DEFAULT_TAX_RATES = {
    "GST": 0.05,
    "PST": 0.07,   # Common in BC
    "HST": 0.13,   # Common in Ontario
    "QST": 0.09975 # Quebec
}

def extract_amount(text):
    match = re.search(r"\$?([\d,]+(?:\.\d{1,2})?)", text)
    if match:
        return float(match.group(1).replace(",", ""))
    return None

def extract_date(text):
    dt = parse_date(text, settings={"PREFER_DATES_FROM": "past"})
    if dt:
        return dt.date().isoformat()
    return None

def extract_vendor(text):
    for key in CATEGORY_KEYWORDS.keys():
        if key.lower() in text.lower():
            return key.capitalize()

    candidates = re.findall(r"\b[A-Z][a-zA-Z0-9]+(?:\s+[A-Z][a-zA-Z0-9]+)?", text)
    for c in candidates:
        if c.lower() not in ["record", "log", "book", "mark", "put"]:
            return c
    return None

def extract_category(text):
    for key, cat in CATEGORY_KEYWORDS.items():
        if key in text.lower():
            return cat
    return None

def extract_taxes(text):
    taxes = {
        "GST": None,
        "PST": None,
        "HST": None,
        "QST": None
    }

    for tax in taxes.keys():
        match = re.search(rf"\$([\d,]+(?:\.\d{{1,2}})?)\s*{tax}", text, re.IGNORECASE)
        if match:
            taxes[tax] = float(match.group(1).replace(",", ""))

    return taxes

def estimate_missing_taxes(subtotal, extracted):
    estimated = {}
    for tax, rate in DEFAULT_TAX_RATES.items():
        if extracted[tax] is None and subtotal is not None:
            estimated[tax] = round(subtotal * rate, 2)
        else:
            estimated[tax] = extracted[tax]
    return estimated

def parse_invoice_command(text):
    subtotal = extract_amount(text)
    vendor = extract_vendor(text)
    category = extract_category(text)
    invoice_date = extract_date(text)
    tax_extracted = extract_taxes(text)
    taxes = estimate_missing_taxes(subtotal, tax_extracted)

    return {
        "amount": subtotal,
        "vendor": vendor,
        "category": category,
        "invoice_date": invoice_date,
        "description": text,
        "status": "staged",
        "taxes": taxes
    }
