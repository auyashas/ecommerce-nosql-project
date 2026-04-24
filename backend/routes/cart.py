from flask import Blueprint, request, jsonify
from services.redis_service import (
    cart_add, cart_set, cart_remove, cart_get, cart_ttl, cart_delete,
)
from services.product_service import get_products_by_ids

bp = Blueprint("cart", __name__, url_prefix="/cart")


def _user_id():
    uid = request.headers.get("X-User-Id") or request.args.get("user_id")
    if not uid:
        return None, (jsonify({"error": "X-User-Id header required"}), 400)
    return uid, None


@bp.post("/add")
def add():
    """POST /cart/add  body: {product_id, qty}"""
    uid, err = _user_id()
    if err:
        return err
    data = request.get_json(force=True) or {}
    product_id = data.get("product_id")
    qty = int(data.get("qty", 1))
    if not product_id:
        return jsonify({"error": "product_id required"}), 400
    cart_add(uid, product_id, qty)
    return jsonify({"message": "Added to cart", "cart": cart_get(uid)})


@bp.post("/update")
def update():
    """POST /cart/update  body: {product_id, qty}  (qty=0 removes item)"""
    uid, err = _user_id()
    if err:
        return err
    data = request.get_json(force=True) or {}
    product_id = data.get("product_id")
    qty = int(data.get("qty", 0))
    if not product_id:
        return jsonify({"error": "product_id required"}), 400
    cart_set(uid, product_id, qty)
    return jsonify({"message": "Cart updated", "cart": cart_get(uid)})


@bp.post("/remove")
def remove():
    """POST /cart/remove  body: {product_id}"""
    uid, err = _user_id()
    if err:
        return err
    data = request.get_json(force=True) or {}
    product_id = data.get("product_id")
    if not product_id:
        return jsonify({"error": "product_id required"}), 400
    cart_remove(uid, product_id)
    return jsonify({"message": "Item removed", "cart": cart_get(uid)})


@bp.post("/clear")
def clear_cart():
    """POST /cart/clear – remove all items from cart."""
    uid, err = _user_id()
    if err:
        return err
    cart_delete(uid)
    return jsonify({"message": "Cart cleared"})


@bp.get("")
def get_cart():
    """GET /cart  – returns cart items enriched with product details."""
    uid, err = _user_id()
    if err:
        return err
    raw = cart_get(uid)
    if not raw:
        return jsonify({"cart": [], "total": 0, "ttl_seconds": 0})

    products = get_products_by_ids(list(raw.keys()))
    items = []
    total = 0.0
    for pid, qty in raw.items():
        p = products.get(pid, {})
        line = round(p.get("price", 0) * qty, 2)
        total += line
        items.append({
            "product_id": pid,
            "name": p.get("name", "Unknown"),
            "price": p.get("price", 0),
            "qty": qty,
            "line_total": line,
            "stock_quantity": p.get("stock_quantity", 0),
            "type": p.get("type"),
        })
    return jsonify({
        "cart": items,
        "total": round(total, 2),
        "ttl_seconds": cart_ttl(uid),
    })
