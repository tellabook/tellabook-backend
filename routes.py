from flask import Blueprint, request, jsonify

bp = Blueprint("main", __name__)

@bp.route("/log-transaction", methods=["POST"])
def log_transaction():
    data = request.get_json()
    message = data.get("message", "")
    user = data.get("user", "")

    # Dummy logic for now
    parsed_data = {
        "category": "insurance",
        "amount": 1400,
        "memo": "truck insurance",
        "user": user
    }

    return jsonify(parsed_data)
