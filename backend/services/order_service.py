"""
Order service – checkout flow: Redis cart → MongoDB order → $inc computed fields.
"""
from datetime import datetime, timezone
from bson import ObjectId
from db import products_col, orders_col
from services.redis_service import cart_get, cart_delete


def now():
    return datetime.now(timezone.utc)


def checkout(user_id: str) -> dict:
    """
    1. Read cart from Redis.
    2. Validate stock for every item.
    3. Create MongoDB order with embedded item snapshots.
    4. $inc stock_quantity (decrement) and computed fields.
    5. Delete Redis cart.
    Returns the created order dict or raises ValueError on failure.
    """
    cart = cart_get(user_id)
    if not cart:
        raise ValueError("Cart is empty")

    product_ids = list(cart.keys())
    oids = [ObjectId(pid) for pid in product_ids]
    products = {str(p["_id"]): p for p in products_col.find({"_id": {"$in": oids}})}

    # ── stock validation ──────────────────────────────────────────────────────
    errors = []
    for pid, qty in cart.items():
        p = products.get(pid)
        if not p:
            errors.append(f"Product {pid} not found")
        elif p["stock_quantity"] < qty:
            errors.append(
                f"'{p['name']}' only has {p['stock_quantity']} in stock "
                f"(requested {qty})"
            )
    if errors:
        raise ValueError("; ".join(errors))

    # ── build order items (snapshot at purchase) ──────────────────────────────
    order_items = []
    total = 0.0
    for pid, qty in cart.items():
        p = products[pid]
        line_total = round(p["price"] * qty, 2)
        total += line_total
        order_items.append({
            "product_id": ObjectId(pid),
            "name": p["name"],
            "price": p["price"],          # snapshot
            "quantity": qty,
            "type": p["type"],
            "line_total": line_total,
        })

    order_doc = {
        "_id": ObjectId(),
        "user_id": ObjectId(user_id) if len(user_id) == 24 else user_id,
        "status": "completed",
        "order_items": order_items,
        "total_amount": round(total, 2),
        "created_at": now(),
    }
    orders_col.insert_one(order_doc)

    # ── Computed Pattern: $inc stock, total_sold, total_revenue ──────────────
    for item in order_items:
        products_col.update_one(
            {"_id": item["product_id"]},
            {"$inc": {
                "stock_quantity": -item["quantity"],
                "computed.total_sold": item["quantity"],
                "computed.total_revenue": item["line_total"],
            }}
        )

    # ── clear Redis cart ──────────────────────────────────────────────────────
    cart_delete(user_id)

    # serialise for response
    order_doc["_id"] = str(order_doc["_id"])
    order_doc["user_id"] = str(order_doc["user_id"])
    for item in order_doc["order_items"]:
        item["product_id"] = str(item["product_id"])
    return order_doc
