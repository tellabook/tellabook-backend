from flask import Blueprint, request, jsonify
from app.models import db, Invoice, UserCommandHistory
from app.parser import parse_invoice

bp = Blueprint("api", __name__)

@bp.route("/invoices", methods=["POST"])
def create_invoice():
    data = request.json

    invoice = Invoice(
        vendor=data.get("vendor"),
        amount=data.get("amount"),
        category=data.get("category"),
        invoice_date=data.get("invoice_date"),
        invoice_number=data.get("invoice_number"),
        description=data.get("description"),
        status="staged"
    )

    db.session.add(invoice)
    db.session.commit()

    return jsonify({"message": "Invoice staged", "invoice_id": invoice.id}), 201


@bp.route("/invoices/staged", methods=["GET"])
def get_staged_invoices():
    invoices = Invoice.query.filter_by(status="staged").all()
    results = [{
        "id": i.id,
        "vendor": i.vendor,
        "amount": i.amount,
        "category": i.category,
        "invoice_date": i.invoice_date.isoformat() if i.invoice_date else None,
        "invoice_number": i.invoice_number,
        "description": i.description,
        "status": i.status,
        "created_at": i.created_at.isoformat()
    } for i in invoices]

    return jsonify(results)


@bp.route("/parse", methods=["POST"])
def parse_and_stage():
    input_text = request.json.get("text")
    parsed_data = parse_invoice(input_text)

    new_invoice = Invoice(
        vendor=parsed_data["vendor"],
        amount=parsed_data["amount"],
        category=parsed_data["category"],
        invoice_date=parsed_data["invoice_date"],
        invoice_number=parsed_data["invoice_number"],
        description=parsed_data["description"],
        status="staged"
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
    })
