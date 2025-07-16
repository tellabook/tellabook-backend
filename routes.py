from flask import Blueprint, request, jsonify

bp = Blueprint("bp", __name__)

@bp.route("/log-transaction", methods=["POST"])
def log_transaction():
    data = request.get_json()
    message = data.get("message")
    user = data.get("user")

    # Just return the values for now — later we’ll connect this to logic
    return jsonify({
        "status": "success",
        "received_message": message,
        "received_user": user
    })
