from flask import Blueprint, request, jsonify
from app.models import db, Invoice, UserCommandHistory
from app.parser import parse_invoice_command  # ✅ Correct function import

bp = Blueprint("api", __name__)

# === POST /invoices — Stage a new invoice manually ===
@bp.route("/invoices", methods=["POST"])
def create_invoice():
    data = request.json

    invoice = Invoice(
        vendor=data.get("vendor"),
        amount=data.get("amount"),
        category=data.get("category"),
        invoice_date=data.get("invoice_date"),
        description=data.get("description"),
        status="staged"
    )

    db.session.add(invoice)
    db.session.commit()

    return jsonify({"message": "Invoice staged", "invoice_id": invoice.id}), 201


# === GET /invoices/staged — Get all staged invoices ===
@bp.route("/invoices/staged", methods=["GET"])
def get_staged_invoices():
    invoices = Invoice.query.filter_by(status="staged").all()

    results = [{
        "id": i.id,
        "vendor": i.vendor,
        "amount": i.amount,
        "category": i.category,
        "invoice_date": i.invoice_date.isoformat() if i.invoice_date else None,
        "description": i.description,
        "status": i.status
    } for i in invoices]

    return jsonify(results), 200


# === PATCH /invoices/<id>/confirm — Mark an invoice as confirmed ===
@bp.route("/invoices/<int:invoice_id>/confirm", methods=["PATCH"])
def confirm_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404

    invoice.status = "confirmed"
    db.session.commit()

    return jsonify({"message": f"Invoice {invoice_id} confirmed"}), 200


# === POST /commands/log — Save what the user said & AI responded ===
@bp.route("/commands/log", methods=["POST"])
def log_command():
    data = request.json

    log = UserCommandHistory(
        input_text=data.get("input_text"),
        output_summary=data.get("output_summary")
    )

    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Command logged", "id": log.id}), 201


# === POST /parse-and-stage — Natural language to staged invoice ===
@bp.route("/parse-and-stage", methods=["POST"])
def parse_and_stage():
    data = request.json
    command = data.get("input_text")

    if not command:
        return jsonify({"error": "Missing input_text"}), 400

    parsed = parse_invoice_command(command)

    invoice = Invoice(
        vendor=parsed.get("vendor"),
        amount=parsed.get("amount"),
        category=parsed.get("category"),
        invoice_date=parsed.get("invoice_date"),
        description=parsed.get("description"),
        status="staged"
    )

    db.session.add(invoice)
    db.session.commit()

    return jsonify({
        "message": "Invoice parsed and staged",
        "invoice_id": invoice.id,
        "parsed_data": parsed
    }), 201
