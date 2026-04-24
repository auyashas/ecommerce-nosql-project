from flask import Blueprint, jsonify
from services.aggregation_service import (
    best_selling_products,
    best_selling_by_category,
    monthly_revenue,
    low_rated_products,
    stock_summary,
)

bp = Blueprint("reports", __name__, url_prefix="/reports")


@bp.get("/best-selling")
def best_selling():
    return jsonify({"best_selling": best_selling_products()})


@bp.get("/best-selling-by-category")
def best_selling_cat():
    return jsonify({"best_selling_by_category": best_selling_by_category()})


@bp.get("/monthly-revenue")
def monthly_rev():
    return jsonify({"monthly_revenue": monthly_revenue()})


@bp.get("/low-rated")
def low_rated():
    threshold = 3.0
    return jsonify({"low_rated_products": low_rated_products(threshold)})


@bp.get("/stock-summary")
def stock():
    return jsonify({"stock_summary": stock_summary()})
