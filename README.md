# ShopSmart – E-Commerce Product Catalog with Smart Cart

Full-stack e-commerce system using **Python/Flask**, **MongoDB**, and **Redis**.

## Stack
| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JS |
| Backend | Python 3.11+ / Flask |
| Product DB | MongoDB (PyMongo) |
| Ephemeral Store | Redis |

---

## Quick Start

### 1. Prerequisites
- MongoDB running on `localhost:27017`
- Redis running on `localhost:6379`
- Python 3.11+

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment (optional)
```bash
cp .env.example .env
# edit .env if your Mongo/Redis are on different hosts
```

### 4. Seed the database (20+ products)
```bash
cd backend
python seed.py
```

### 5. Start the API
```bash
cd backend
python app.py
# API runs on http://localhost:5000
```

### 6. Open the frontend
Open `frontend/index.html` in your browser (or serve with any static server).

---

## MongoDB Schema Design

### Polymorphic Pattern – `products` collection
All products share a common base; type-specific fields are added per document type.

```
Common fields: name, price, category, brand, stock_quantity, type, computed, created_at

Electronics extras: warranty_years, specs {driver, battery_hours, ...}
Book extras:        author, isbn, pages
Clothing extras:    sizes[], colors[], material
```

### Computed Pattern – `products.computed`
Updated via `$inc` on every purchase/review — no expensive aggregations at read time.
```json
{
  "total_sold": 12,
  "avg_rating": 4.5,
  "review_count": 8,
  "total_revenue": 4199.88
}
```

### Orders – Reference + Embedded Snapshot
```json
{
  "user_id": ObjectId,          // reference
  "order_items": [              // embedded snapshot at purchase time
    { "product_id": ObjectId, "name": "...", "price": 349.99, "quantity": 2 }
  ],
  "total_amount": 699.98,
  "status": "completed"
}
```

### Reviews – Separate Collection
Kept separate to avoid unbounded array growth on product documents.

---

## Redis Data Structures

| Feature | Key Pattern | Structure | TTL |
|---------|------------|-----------|-----|
| Shopping Cart | `cart:<userId>` | Hash `{productId: qty}` | 24 h |
| View Counter | `views:<productId>` | String (integer) | 24 h |
| Trending | `trending` | Sorted Set `{productId: score}` | 1 h |
| Recently Viewed | `recently_viewed:<userId>` | List (last 10) | — |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/products` | List products (filter by type, category, brand, price, rating) |
| GET | `/products/<id>` | Product detail (triggers view counter + trending) |
| GET | `/products/<id>/reviews` | Get paginated reviews for a product |
| POST | `/products/<id>/reviews` | Submit a review (recomputes avg_rating) |
| POST | `/cart/add` | Add item to cart |
| POST | `/cart/update` | Update item quantity |
| POST | `/cart/remove` | Remove item from cart |
| POST | `/cart/clear` | Clear entire cart |
| GET | `/cart` | Get cart with product details |
| POST | `/checkout` | Redis cart → MongoDB order + stock validation |
| GET | `/trending` | Top 10 trending products (Sorted Set) |
| GET | `/recently-viewed` | Last 10 viewed by user (List) |
| GET | `/reports/best-selling` | Top products by total_sold |
| GET | `/reports/best-selling-by-category` | Aggregated by category |
| GET | `/reports/monthly-revenue` | Revenue grouped by month |
| GET | `/reports/low-rated` | Products with avg_rating < 3 |
| GET | `/reports/stock-summary` | Stock levels by category |

All cart/checkout/recently-viewed endpoints require `X-User-Id` header.

---

## Frontend Pages

| Page | File | Description |
|------|------|-------------|
| Catalog | `index.html` | Product grid with filters + recently viewed |
| Product Detail | `product.html` | Full detail, specs, reviews, add to cart |
| Cart | `cart.html` | Cart items, quantities, clear cart, checkout link |
| Checkout | `checkout.html` | Order review + place order (stock validated) |
| Trending | `trending.html` | Trending Now board + recently viewed |
| Reports | `reports.html` | Analytics dashboard with 5 aggregation reports |

---
1. `POST /checkout` reads cart from Redis (`HGETALL cart:<userId>`)
2. Validates stock for every item — returns 400 with error if insufficient
3. Creates MongoDB order with embedded item snapshots (price locked at purchase)
4. `$inc` on `stock_quantity`, `computed.total_sold`, `computed.total_revenue`
5. Deletes Redis cart (`DEL cart:<userId>`)

---

## Postman Collection