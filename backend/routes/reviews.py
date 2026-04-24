"""
Reviews endpoints.
GET  /products/<id>/reviews  – paginated reviews for a product
POST /products/<id>/reviews  – submit a review (updates computed avg_rating)
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId
from db import reviews_col, products_col

bp = Blueprint("reviews", __name__)


def _now():
    return datetime.now(timezone.utc)


def _oid(s):
    try:
        return ObjectId(s)
    except (InvalidId, TypeError):
        return None


@bp.get("/products/<product_id>/reviews")
def get_reviews(product_id):
    oid = _oid(product_id)
    if not oid:
        return jsonify({"error": "Invalid product id"}), 400

    page  = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    skip  = (page - 1) * limit

    cursor = (
        reviews_col.find({"product_id": oid})
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
    )
    total = reviews_col.count_documents({"product_id": oid})
    reviews = []
    for r in cursor:
        r["_id"]        = str(r["_id"])
        r["product_id"] = str(r["product_id"])
        r["user_id"]    = str(r["user_id"])
        reviews.append(r)

    return jsonify({
        "reviews": reviews,
        "total": total,
        "page": page,
        "pages": max(1, -(-total // limit)),   # ceiling division
    })


@bp.post("/products/<product_id>/reviews")
def add_review(product_id):
    oid = _oid(product_id)
    if not oid:
        return jsonify({"error": "Invalid product id"}), 400

    if not products_col.find_one({"_id": oid}):
        return jsonify({"error": "Product not found"}), 404

    data   = request.get_json(force=True) or {}
    rating = data.get("rating")
    text   = data.get("text", "").strip()
    user_id = request.headers.get("X-User-Id", "anonymous")

    if rating is None or not (1 <= int(rating) <= 5):
        return jsonify({"error": "rating must be 1–5"}), 400

    rating = int(rating)

    # Insert review
    review = {
        "_id":        ObjectId(),
        "product_id": oid,
        "user_id":    user_id,
        "rating":     rating,
        "text":       text,
        "created_at": _now(),
    }
    reviews_col.insert_one(review)

    # Recompute avg_rating and review_count via aggregation, then $set
    pipeline = [
        {"$match": {"product_id": oid}},
        {"$group": {
            "_id":          "$product_id",
            "avg_rating":   {"$avg": "$rating"},
            "review_count": {"$sum": 1},
        }},
    ]
    agg = list(reviews_col.aggregate(pipeline))
    if agg:
        products_col.update_one(
            {"_id": oid},
            {"$set": {
                "computed.avg_rating":   round(agg[0]["avg_rating"], 2),
                "computed.review_count": agg[0]["review_count"],
            }}
        )

    review["_id"]        = str(review["_id"])
    review["product_id"] = str(review["product_id"])
    return jsonify({"message": "Review submitted", "review": review}), 201
