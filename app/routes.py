from flask import Blueprint, request, jsonify
from app.parser import parse_invoice
from app.models import db, Invoice, UserCommandHistory

bp = Blueprint("routes", __name__)

@bp.route("/parse-and-stage", methods=["POST"])
def parse_and_stage():
    data = request.get_json()
    input_text = data.get("input_text", "")

    if not input_text:
        return jsonify({"error": "No input text provided."}), 400

    parsed_data = parse_invoice(input_text)

    new_invoice = Invoice(
        amount=parsed_data["amount"],
        category=parsed_data["category"],
        invoice_date=parsed_data["invoice_date"],
        invoice_number=parsed_data["invoice_number"],
        description=parsed_data["description"],
        status=parsed_data["status"],
        vendor=parsed_data["vendor"]
    )
    db.session.add(new_invoice)

    command_history = UserCommandHistory(
        input_text=input_text,
        output_summary=parsed_data["description"]
    )
    db.session.add(command_history)

    db.session.commit()

    return jsonify({
        "message": "Invoice parsed and staged",
        "invoice_id": new_invoice.id,
        "parsed_data": parsed_data
    }), 201
