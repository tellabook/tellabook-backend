import re
from dateparser import parse as parse_date
from datetime import datetime

# Keyword mappings
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

# Tax patterns to extract exact tax types
TAX_PATTERNS = {
    "GST": r"\$?([\d,]+\.\d{1,2}|\d+)\s*GST",
    "PST": r"\$?([\d,]+\.\d{1,2}|\d+)\s*PST",
    "HST": r"\$?([\d,]+\.\d{1,2}|\d+)\s*HST",
    "QST": r"\$?([\d,]+\.\d{1,2}|\d+)\s*QST"
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
    return datetime.today().date().isoformat()  # Default to today

def extract_vendor(text):
    for key in CATEGORY_KEYWORDS:
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
    taxes = {}
    for tax_type, pattern in TAX_PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount = float(match.group(1).replace(",", ""))
            taxes[tax_type] = amount
    return taxes if taxes else None

def parse_invoice_command(text):
    return {
        "amount": extract_amount(text),
        "vendor": extract_vendor(text),
        "category": extract_category(text),
        "invoice_date": extract_date(text),
        "taxes": extract_taxes(text),
        "description": text,
        "status": "staged"
    }
