from flask import Blueprint, request, jsonify
from services.redis_service import get_trending, get_recently_viewed
from services.product_service import get_products_by_ids

bp = Blueprint("trending", __name__)


@bp.get("/trending")
def trending():
    """GET /trending – Top 10 products by view score (hourly Sorted Set)."""
    top = get_trending(10)
    if not top:
        return jsonify({"trending": []})
    ids = [t["product_id"] for t in top]
    products = get_products_by_ids(ids)
    result = []
    for t in top:
        p = products.get(t["product_id"], {})
        result.append({
            "product_id": t["product_id"],
            "score": t["score"],
            "name": p.get("name", "Unknown"),
            "price": p.get("price"),
            "type": p.get("type"),
        })
    return jsonify({"trending": result})


@bp.get("/recently-viewed")
def recently_viewed():
    """GET /recently-viewed – Last 10 products viewed by user."""
    uid = request.headers.get("X-User-Id") or request.args.get("user_id", "anonymous")
    ids = get_recently_viewed(uid)
    if not ids:
        return jsonify({"recently_viewed": []})
    products = get_products_by_ids(ids)
    # preserve order
    result = []
    for pid in ids:
        p = products.get(pid, {})
        if p:
            result.append(p)
    return jsonify({"recently_viewed": result})
