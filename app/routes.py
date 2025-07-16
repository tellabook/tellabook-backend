from flask import Blueprint, request, jsonify
from .logic import interpret_transaction

bp = Blueprint('api', __name__)

@bp.route('/log-transaction', methods=['POST'])
def log_transaction():
    user_input = request.json.get("input")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    result = interpret_transaction(user_input)
    return jsonify(result)
