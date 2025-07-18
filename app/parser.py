import re
from datetime import datetime
import dateparser

def parse_invoice_command(command):
    result = {
        "vendor": None,
        "amount": None,
        "category": None,
        "invoice_date": datetime.today().date(),  # Default to today
        "description": None,
        "invoice_number": None,
        "taxes": {
            "GST": 0.0,
            "PST": 0.0,
            "HST": 0.0,
            "QST": 0.0,
        }
    }

    # Amount
    amount_match = re.search(r"\$?([\d,]+(?:\.\d{1,2})?)", command)
    if amount_match:
        result["amount"] = float(amount_match.group(1).replace(",", ""))

    # Vendor (first capitalized word after "for" or "to")
    vendor_match = re.search(r"(?:for|to)\s+([A-Z][\w\s&-]{1,40})", command)
    if vendor_match:
        result["vendor"] = vendor_match.group(1).strip()

    # Date
    date = dateparser.search.search_dates(command)
    if date:
        result["invoice_date"] = date[0][1].date()

    # Invoice number
    invoice_no = re.search(r"invoice (?:number\s*)?#?(\d+)", command, re.IGNORECASE)
    if invoice_no:
        result["invoice_number"] = invoice_no.group(1)

    # Taxes
    for tax in ["GST", "PST", "HST", "QST"]:
        match = re.search(r"\$([\d,]+(?:\.\d{1,2})?)\s*" + tax, command, re.IGNORECASE)
        if match:
            result["taxes"][tax] = float(match.group(1).replace(",", ""))

    # Category guess
    if "lease" in command.lower() or "rent" in command.lower():
        result["category"] = "Lease Expense"
    elif "fuel" in command.lower() or "gas" in command.lower():
        result["category"] = "Fuel"
    elif "repair" in command.lower():
        result["category"] = "Repairs"
    elif "insurance" in command.lower():
        result["category"] = "Insurance"
    elif "meal" in command.lower() or "restaurant" in command.lower():
        result["category"] = "Meals & Entertainment"
    else:
        result["category"] = "Uncategorized"

    # Description summary
    result["description"] = summarize_description(command)

    return result

def summarize_description(text):
    text = re.sub(r"\s+", " ", text.strip())
    if len(text) > 80:
        return text[:77] + "..."
    return text
