from flask import Blueprint, request, jsonify
from services.order_service import checkout

bp = Blueprint("checkout", __name__, url_prefix="/checkout")


@bp.post("")
def do_checkout():
    """
    POST /checkout
    Reads cart from Redis, validates stock, creates MongoDB order,
    updates computed fields, deletes Redis cart.
    """
    uid = request.headers.get("X-User-Id") or (request.get_json(force=True) or {}).get("user_id")
    if not uid:
        return jsonify({"error": "X-User-Id header required"}), 400
    try:
        order = checkout(uid)
        return jsonify({"message": "Order placed successfully", "order": order}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
