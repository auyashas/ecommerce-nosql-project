"""
Aggregation reports – best-selling, monthly revenue, low-rated, stock summary.
"""
from db import products_col, orders_col


def best_selling_products(limit: int = 10) -> list[dict]:
    """Top N products by total_sold (Computed Pattern)."""
    cursor = (
        products_col.find({}, {"name": 1, "computed.total_sold": 1, "price": 1})
        .sort("computed.total_sold", -1)
        .limit(limit)
    )
    return [_serialize(p) for p in cursor]


def best_selling_by_category() -> list[dict]:
    """Aggregate total_sold grouped by category."""
    pipeline = [
        {"$group": {
            "_id": "$category",
            "total_sold": {"$sum": "$computed.total_sold"},
            "total_revenue": {"$sum": "$computed.total_revenue"},
        }},
        {"$sort": {"total_sold": -1}},
    ]
    return list(products_col.aggregate(pipeline))


def monthly_revenue() -> list[dict]:
    """Aggregate order total_amount by year-month."""
    pipeline = [
        {"$group": {
            "_id": {
                "year": {"$year": "$created_at"},
                "month": {"$month": "$created_at"},
            },
            "revenue": {"$sum": "$total_amount"},
            "order_count": {"$sum": 1},
        }},
        {"$sort": {"_id.year": -1, "_id.month": -1}},
    ]
    return list(orders_col.aggregate(pipeline))


def low_rated_products(threshold: float = 3.0) -> list[dict]:
    """Products with avg_rating below threshold and at least 1 review."""
    cursor = products_col.find(
        {
            "computed.avg_rating": {"$lt": threshold, "$gt": 0},
            "computed.review_count": {"$gte": 1},
        },
        {"name": 1, "computed.avg_rating": 1, "computed.review_count": 1}
    )
    return [_serialize(p) for p in cursor]


def stock_summary() -> list[dict]:
    """Aggregate stock by category."""
    pipeline = [
        {"$group": {
            "_id": "$category",
            "total_stock": {"$sum": "$stock_quantity"},
            "product_count": {"$sum": 1},
        }},
        {"$sort": {"total_stock": -1}},
    ]
    return list(products_col.aggregate(pipeline))


def _serialize(doc: dict) -> dict:
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc
