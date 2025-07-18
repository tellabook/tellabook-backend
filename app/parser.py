import re
from datetime import datetime
import dateparser

def parse_invoice(input_text):
    result = {
        "amount": None,
        "category": None,
        "description": None,
        "invoice_date": None,
        "status": "staged",
        "vendor": None,
        "taxes": {},
        "invoice_number": None
    }

    # Extract amount
    amount_match = re.search(r"\$?(\d{1,3}(?:,\d{3})*|\d+)(?:\.\d{2})?", input_text)
    if amount_match:
        amount = float(amount_match.group().replace('$', '').replace(',', ''))
        result["amount"] = amount

    # Extract vendor
    vendor_match = re.search(r"for\s+([A-Za-z0-9 &\-]+?)(?:\s+from|\s+on|\s+dated|\s+due|\s+starting|,|$)", input_text, re.IGNORECASE)
    if vendor_match:
        result["vendor"] = vendor_match.group(1).strip().title()

    # Extract invoice number
    invoice_number_match = re.search(r"(?:invoice\s*(?:number)?\s*(?:is)?\s*#?\s*)(\d+)", input_text, re.IGNORECASE)
    if invoice_number_match:
        result["invoice_number"] = invoice_number_match.group(1)

    # Extract date
    date_match = dateparser.search.search_dates(input_text)
    if date_match:
        result["invoice_date"] = date_match[0][1].date().isoformat()
    else:
        result["invoice_date"] = datetime.today().date().isoformat()

    # Extract taxes
    tax_keywords = {
        "GST": r"\$([\d,]+(?:\.\d{2})?)\s*GST",
        "PST": r"\$([\d,]+(?:\.\d{2})?)\s*PST",
        "HST": r"\$([\d,]+(?:\.\d{2})?)\s*HST",
        "QST": r"\$([\d,]+(?:\.\d{2})?)\s*QST"
    }
    for tax_type, pattern in tax_keywords.items():
        match = re.search(pattern, input_text, re.IGNORECASE)
        if match:
            result["taxes"][tax_type] = float(match.group(1).replace(',', ''))

    # Guess category from keywords
    keywords_to_categories = {
        "internet": "Internet",
        "lease": "Lease Expense",
        "rent": "Lease Expense",
        "payroll": "Payroll",
        "software": "Software",
        "equipment": "Equipment Purchase",
        "truck": "Vehicle Expense",
        "fuel": "Fuel",
        "advertising": "Advertising",
        "consulting": "Professional Fees"
    }
    for word, category in keywords_to_categories.items():
        if re.search(rf"\b{word}\b", input_text, re.IGNORECASE):
            result["category"] = category
            break

    # Description summary
    summary_parts = []
    if result["amount"]:
        summary_parts.append(f"${result['amount']:.2f}")
    if result["vendor"]:
        summary_parts.append(f"to {result['vendor']}")
    if result["category"]:
        summary_parts.append(f"for {result['category']}")
    if result["invoice_date"]:
        summary_parts.append(f"on {result['invoice_date']}")

    result["description"] = " ".join(summary_parts)

    return result
