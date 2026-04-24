from flask import Blueprint, request, jsonify
from services.product_service import list_products, get_product
from services.redis_service import increment_view, get_views, trending_increment, push_recently_viewed

bp = Blueprint("products", __name__, url_prefix="/products")


@bp.get("")
def index():
    """
    GET /products
    Query params: type, category, brand, min_price, max_price, min_rating,
                  sort_by, order (1/-1), limit, skip
    """
    params = request.args
    products = list_products(
        type_=params.get("type"),
        category=params.get("category"),
        brand=params.get("brand"),
        min_price=params.get("min_price"),
        max_price=params.get("max_price"),
        min_rating=params.get("min_rating"),
        sort_by=params.get("sort_by", "created_at"),
        order=int(params.get("order", -1)),
        limit=int(params.get("limit", 50)),
        skip=int(params.get("skip", 0)),
    )
    return jsonify({"products": products, "count": len(products)})


@bp.get("/<product_id>")
def detail(product_id):
    """
    GET /products/<id>
    Triggers view counter + trending increment + recently viewed push.
    Requires header X-User-Id for recently viewed tracking.
    """
    product = get_product(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Redis side-effects
    views = increment_view(product_id)
    trending_increment(product_id)

    user_id = request.headers.get("X-User-Id", "anonymous")
    push_recently_viewed(user_id, product_id)

    product["daily_views"] = views
    return jsonify(product)
