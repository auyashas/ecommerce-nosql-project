"""
E-Commerce Product Catalog API
Flask + MongoDB (PyMongo) + Redis
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from routes.products  import bp as products_bp
from routes.cart      import bp as cart_bp
from routes.checkout  import bp as checkout_bp
from routes.trending  import bp as trending_bp
from routes.reports   import bp as reports_bp
from routes.reviews   import bp as reviews_bp

# Point Flask's static folder at frontend/static so
# /static/css/style.css and /static/js/api.js resolve correctly
app = Flask(__name__, static_folder=os.path.join(FRONTEND_DIR, "static"), static_url_path="/static")
CORS(app)

# ── API blueprints ────────────────────────────────────────────────────────────
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(trending_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(reviews_bp)

# ── Frontend pages ────────────────────────────────────────────────────────────
PAGES = ["index.html", "product.html", "cart.html",
         "checkout.html", "trending.html", "reports.html"]

@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route('/<path:filename>')
def serve_static_pages(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# ── API health ────────────────────────────────────────────────────────────────
@app.get("/api")
def health():
    return jsonify({
        "status": "ok",
        "endpoints": [
            "GET  /products", "GET  /products/<id>",
            "POST /cart/add", "POST /cart/update",
            "POST /cart/remove", "POST /cart/clear", "GET  /cart",
            "POST /checkout",
            "GET  /trending", "GET  /recently-viewed",
            "GET  /products/<id>/reviews", "POST /products/<id>/reviews",
            "GET  /reports/best-selling", "GET  /reports/best-selling-by-category",
            "GET  /reports/monthly-revenue", "GET  /reports/low-rated",
            "GET  /reports/stock-summary",
        ]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
