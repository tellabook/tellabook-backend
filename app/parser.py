import re
from datetime import date
from dateparser.search import search_dates

# === CATEGORY & VENDOR HINTS ===
CATEGORY_KEYWORDS = {
    "Internet": ["telus", "shaw", "rogers", "internet"],
    "Phone": ["bell", "fido", "rogers", "phone", "mobility"],
    "Insurance": ["insurance", "aviva", "intact", "policy"],
    "Fuel": ["fuel", "gas", "diesel", "petro", "esso", "shell"],
    "Lease Expense": ["lease", "leasing", "rent"],
    "Office Supplies": ["staples", "office", "supplies", "stationery"],
    "Meals & Entertainment": ["restaurant", "meal", "dinner", "lunch", "coffee", "entertainment"],
    "Software": ["microsoft", "adobe", "software", "saas", "subscription", "quickbooks"],
    "Repairs & Maintenance": ["repair", "maintenance", "service", "fix"],
    "Professional Fees": ["lawyer", "accountant", "consulting", "bookkeeping", "legal"],
    "Advertising": ["marketing", "ad", "advertising", "promotion"],
    "Bank Charges": ["bank", "interest", "charge", "fee"],
    "Travel": ["flight", "hotel", "uber", "airbnb", "taxi", "car rental"]
}

def infer_category(text):
    text_lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            return category
    return "Uncategorized"

def extract_vendor(text):
    words = re.findall(r'\b[A-Z][a-zA-Z]+\b', text)
    common_exclude = {"Record", "Invoice", "Amount", "From", "For", "The", "And"}
    for word in words:
        if word not in common_exclude:
            return word
    return "Unknown"

def extract_amount(text):
    match = re.search(r"\$?([0-9,]+\.?\d{0,2})", text)
    if match:
        return float(match.group(1).replace(",", ""))
    return 0.0

def extract_invoice_number(text):
    match = re.search(r"invoice number is (\d+)", text.lower())
    return match.group(1) if match else None

def extract_taxes(text):
    taxes = {}
    for tax in ["GST", "PST", "HST", "QST"]:
        match = re.search(rf"\$?([0-9,]+\.?\d{{0,2}})\s*{tax}", text, re.IGNORECASE)
        if match:
            amount = float(match.group(1).replace(",", ""))
            taxes[tax.upper()] = amount
    return taxes if taxes else None

def extract_date(text):
    found = search_dates(text, settings={"PREFER_DATES_FROM": "past"})
    if found:
        # Return the first matched date
        return found[0][1].date().isoformat()
    return date.today().isoformat()

def summarize_description(text):
    summary = text.lower()
    if "lease" in summary and "truck" in summary:
        return "Truck lease payment"
    elif "internet" in summary:
        return "Internet bill"
    elif "insurance" in summary:
        return "Insurance expense"
    elif "gst" in summary or "pst" in summary:
        return "Expense with sales taxes"
    return "Business expense"

# === MAIN PARSER FUNCTION ===
def parse_invoice_command(text):
    return {
        "amount": extract_amount(text),
        "category": infer_category(text),
        "vendor": extract_vendor(text),
        "invoice_date": extract_date(text),
        "invoice_number": extract_invoice_number(text),
        "description": summarize_description(text),
        "taxes": extract_taxes(text),
        "status": "staged"
    }
