import re
from datetime import datetime
from dateparser.search import search_dates

def parse_invoice(text):
    result = {}

    # Extract amount
    amount_match = re.search(r"\$?([\d,]+(?:\.\d{1,2})?)", text)
    if amount_match:
        result["amount"] = float(amount_match.group(1).replace(",", ""))
    else:
        result["amount"] = 0.0

    # Extract GST, PST, HST, QST
    taxes = {}
    gst_match = re.search(r"\$([\d,]+(?:\.\d{1,2})?)\s*GST", text, re.IGNORECASE)
    pst_match = re.search(r"\$([\d,]+(?:\.\d{1,2})?)\s*PST", text, re.IGNORECASE)
    hst_match = re.search(r"\$([\d,]+(?:\.\d{1,2})?)\s*HST", text, re.IGNORECASE)
    qst_match = re.search(r"\$([\d,]+(?:\.\d{1,2})?)\s*QST", text, re.IGNORECASE)

    if gst_match:
        taxes["GST"] = float(gst_match.group(1).replace(",", ""))
    if pst_match:
        taxes["PST"] = float(pst_match.group(1).replace(",", ""))
    if hst_match:
        taxes["HST"] = float(hst_match.group(1).replace(",", ""))
    if qst_match:
        taxes["QST"] = float(qst_match.group(1).replace(",", ""))

    if taxes:
        result["taxes"] = taxes

    # Extract date
    date = search_dates(text)
    if date:
        result["invoice_date"] = date[0][1].date().isoformat()
    else:
        result["invoice_date"] = datetime.now().date().isoformat()

    # Extract invoice number
    invoice_number_match = re.search(r"invoice\s+(?:#|number)?\s*(\d+)", text, re.IGNORECASE)
    if invoice_number_match:
        result["invoice_number"] = invoice_number_match.group(1)

    # Category
    if "lease" in text.lower():
        result["category"] = "Lease Expense"
    elif "truck" in text.lower():
        result["category"] = "Truck Expense"
    elif "repair" in text.lower():
        result["category"] = "Repairs & Maintenance"
    elif "legal" in text.lower():
        result["category"] = "Legal & Professional"
    else:
        result["category"] = "General Expense"

    # Vendor from month name or fallback
    months = [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december"
    ]
    result["vendor"] = next((m.capitalize() for m in months if m in text.lower()), "Unknown Vendor")

    # Description
    result["description"] = f"{result['category']} for {result['vendor']}"

    return result
