"""
Product service – MongoDB queries with Polymorphic Pattern support.
"""
from bson import ObjectId
from bson.errors import InvalidId
from db import products_col


def _oid(id_str: str):
    try:
        return ObjectId(id_str)
    except (InvalidId, TypeError):
        return None


def build_filter(type_=None, category=None, brand=None,
                 min_price=None, max_price=None, min_rating=None):
    f = {}
    if type_:
        f["type"] = type_
    if category:
        f["category"] = {"$regex": category, "$options": "i"}
    if brand:
        f["brand"] = {"$regex": brand, "$options": "i"}
    price_filter = {}
    if min_price is not None:
        price_filter["$gte"] = float(min_price)
    if max_price is not None:
        price_filter["$lte"] = float(max_price)
    if price_filter:
        f["price"] = price_filter
    if min_rating is not None:
        f["computed.avg_rating"] = {"$gte": float(min_rating)}
    return f


def list_products(type_=None, category=None, brand=None,
                  min_price=None, max_price=None, min_rating=None,
                  sort_by="created_at", order=-1, limit=50, skip=0):
    f = build_filter(type_, category, brand, min_price, max_price, min_rating)
    cursor = (
        products_col.find(f)
        .sort(sort_by, order)
        .skip(skip)
        .limit(limit)
    )
    return [_serialize(p) for p in cursor]


def get_product(product_id: str):
    oid = _oid(product_id)
    if not oid:
        return None
    p = products_col.find_one({"_id": oid})
    return _serialize(p) if p else None


def get_products_by_ids(ids: list[str]) -> dict:
    """Return {str_id: product_doc} for a list of id strings."""
    oids = [_oid(i) for i in ids if _oid(i)]
    docs = products_col.find({"_id": {"$in": oids}})
    return {str(d["_id"]): _serialize(d) for d in docs}


def _serialize(doc: dict) -> dict:
    if doc is None:
        return {}
    doc["_id"] = str(doc["_id"])
    return doc
