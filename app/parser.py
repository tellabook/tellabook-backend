import re
from dateparser import parse as parse_date
from datetime import datetime

# Basic keyword maps
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
    # Look for known vendor keywords first
    for key in CATEGORY_KEYWORDS.keys():
        if key.lower() in text.lower():
            return key.capitalize()

    # Otherwise, look for the first capitalized word that's not a verb
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

def parse_invoice_command(text):
    return {
        "amount": extract_amount(text),
        "vendor": extract_vendor(text),
        "category": extract_category(text),
        "invoice_date": extract_date(text),
        "description": text,
        "status": "staged"
    }
