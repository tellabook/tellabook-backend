import re
from datetime import datetime
from dateparser.search import search_dates


def parse_invoice(input_text):
    result = {
        "amount": None,
        "category": "Lease Expense",
        "description": "",
        "invoice_date": None,
        "invoice_number": None,
        "status": "staged",
        "taxes": [],
        "vendor": None
    }

    result["description"] = summarize_description(input_text)

    amount_match = re.search(r"\$([\d,]+\.?\d*)", input_text)
    if amount_match:
        result["amount"] = float(amount_match.group(1).replace(",", ""))

    invoice_match = re.search(r"invoice number is (\d+)", input_text, re.IGNORECASE)
    if invoice_match:
        result["invoice_number"] = invoice_match.group(1)

    tax_matches = re.findall(r"\$(\d+(?:\.\d{1,2})?)\s+(GST|PST|HST|QST)", input_text, re.IGNORECASE)
    for value, tax_type in tax_matches:
        result["taxes"].append({tax_type.upper(): float(value)})

    dates = search_dates(input_text)
    if dates:
        result["invoice_date"] = dates[0][1].date().isoformat()
    else:
        result["invoice_date"] = datetime.today().date().isoformat()

    vendor_match = re.search(r"from ([A-Z][a-z]+ \d{1,2})", input_text)
    if vendor_match:
        result["vendor"] = vendor_match.group(1)

    return result

def summarize_description(text):
    return " ".join(text.strip().split()[:7]) + "..."