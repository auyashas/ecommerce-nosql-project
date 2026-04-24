"""
Seed script – inserts 20+ products (Electronics, Books, Clothing),
a demo user, sample reviews, and demonstrates the Computed Pattern.
Run once: python seed.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timezone
from bson import ObjectId
from db import products_col, orders_col, reviews_col, users_col, ensure_indexes

# ── helpers ───────────────────────────────────────────────────────────────────
def now():
    return datetime.now(timezone.utc)

def pid():
    return ObjectId()

# ── wipe existing data ────────────────────────────────────────────────────────
products_col.drop()
orders_col.drop()
reviews_col.drop()
users_col.drop()
ensure_indexes()

# ── demo user ─────────────────────────────────────────────────────────────────
user_id = ObjectId()
users_col.insert_one({
    "_id": user_id,
    "name": "Alice Demo",
    "email": "alice@example.com",
    "created_at": now(),
})

# ── products ──────────────────────────────────────────────────────────────────
# Computed Pattern fields are initialised to 0 and updated via $inc on purchase/review.
def computed():
    return {"total_sold": 0, "avg_rating": 0.0, "review_count": 0, "total_revenue": 0.0}

electronics = [
    {
        "_id": pid(), "type": "electronics",
        "name": "Sony WH-1000XM5 Headphones", "price": 29990,
        "category": "Audio", "brand": "Sony", "stock_quantity": 45,
        "warranty_years": 2,
        "specs": {"driver": "30mm", "battery_hours": 30, "noise_cancelling": True, "connectivity": "Bluetooth 5.2"},
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "electronics",
        "name": "Apple MacBook Air M3", "price": 114900,
        "category": "Laptops", "brand": "Apple", "stock_quantity": 20,
        "warranty_years": 1,
        "specs": {"cpu": "Apple M3", "ram_gb": 16, "storage_gb": 512, "display_inch": 13.6},
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "electronics",
        "name": "Samsung 65\" QLED TV", "price": 89990,
        "category": "TVs", "brand": "Samsung", "stock_quantity": 12,
        "warranty_years": 3,
        "specs": {"resolution": "4K", "refresh_rate_hz": 120, "hdr": "HDR10+", "smart": True},
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "electronics",
        "name": "Logitech MX Master 3S Mouse", "price": 8495,
        "category": "Peripherals", "brand": "Logitech", "stock_quantity": 80,
        "warranty_years": 2,
        "specs": {"dpi": 8000, "buttons": 7, "wireless": True, "battery_days": 70},
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "electronics",
        "name": "GoPro HERO12 Black", "price": 34990,
        "category": "Cameras", "brand": "GoPro", "stock_quantity": 30,
        "warranty_years": 1,
        "specs": {"video": "5.3K60", "waterproof_m": 10, "stabilisation": "HyperSmooth 6.0"},
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "electronics",
        "name": "iPad Pro 12.9\" M4", "price": 99900,
        "category": "Tablets", "brand": "Apple", "stock_quantity": 25,
        "warranty_years": 1,
        "specs": {"cpu": "Apple M4", "storage_gb": 256, "display": "Liquid Retina XDR", "5g": True},
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "electronics",
        "name": "Bose QuietComfort Ultra Earbuds", "price": 24900,
        "category": "Audio", "brand": "Bose", "stock_quantity": 55,
        "warranty_years": 1,
        "specs": {"battery_hours": 6, "case_hours": 24, "anc": True, "spatial_audio": True},
        "computed": computed(), "created_at": now(),
    },
]

books = [
    {
        "_id": pid(), "type": "book",
        "name": "Clean Code", "price": 799,
        "category": "Programming", "brand": "Prentice Hall", "stock_quantity": 100,
        "author": "Robert C. Martin", "isbn": "978-0132350884", "pages": 431,
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "book",
        "name": "Designing Data-Intensive Applications", "price": 1299,
        "category": "Programming", "brand": "O'Reilly", "stock_quantity": 75,
        "author": "Martin Kleppmann", "isbn": "978-1449373320", "pages": 616,
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "book",
        "name": "The Pragmatic Programmer", "price": 999,
        "category": "Programming", "brand": "Addison-Wesley", "stock_quantity": 90,
        "author": "David Thomas & Andrew Hunt", "isbn": "978-0135957059", "pages": 352,
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "book",
        "name": "Atomic Habits", "price": 399,
        "category": "Self-Help", "brand": "Avery", "stock_quantity": 200,
        "author": "James Clear", "isbn": "978-0735211292", "pages": 320,
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "book",
        "name": "Deep Work", "price": 349,
        "category": "Self-Help", "brand": "Grand Central", "stock_quantity": 150,
        "author": "Cal Newport", "isbn": "978-1455586691", "pages": 296,
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "book",
        "name": "MongoDB: The Definitive Guide", "price": 1199,
        "category": "Databases", "brand": "O'Reilly", "stock_quantity": 60,
        "author": "Shannon Bradshaw", "isbn": "978-1491954461", "pages": 514,
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "book",
        "name": "Python Crash Course", "price": 699,
        "category": "Programming", "brand": "No Starch Press", "stock_quantity": 120,
        "author": "Eric Matthes", "isbn": "978-1718502703", "pages": 552,
        "computed": computed(), "created_at": now(),
    },
]

clothing = [
    {
        "_id": pid(), "type": "clothing",
        "name": "Nike Air Max 270", "price": 10995,
        "category": "Footwear", "brand": "Nike", "stock_quantity": 60,
        "sizes": ["UK 6", "UK 7", "UK 8", "UK 9", "UK 10"],
        "colors": ["Black/White", "White/Red", "Grey/Blue"],
        "material": "Mesh upper, foam midsole",
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "clothing",
        "name": "Levi's 501 Original Jeans", "price": 3999,
        "category": "Bottoms", "brand": "Levi's", "stock_quantity": 85,
        "sizes": ["28x30", "30x30", "32x32", "34x32", "36x34"],
        "colors": ["Dark Wash", "Light Wash", "Black"],
        "material": "100% Cotton Denim",
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "clothing",
        "name": "Patagonia Nano Puff Jacket", "price": 19999,
        "category": "Outerwear", "brand": "Patagonia", "stock_quantity": 40,
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colors": ["Black", "Navy", "Forest Green"],
        "material": "100% recycled polyester",
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "clothing",
        "name": "Adidas Ultraboost 23", "price": 14999,
        "category": "Footwear", "brand": "Adidas", "stock_quantity": 50,
        "sizes": ["UK 6", "UK 7", "UK 8", "UK 9", "UK 10", "UK 11"],
        "colors": ["Core Black", "Cloud White", "Solar Red"],
        "material": "Primeknit+ upper, Boost midsole",
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "clothing",
        "name": "Champion Reverse Weave Hoodie", "price": 3499,
        "category": "Tops", "brand": "Champion", "stock_quantity": 110,
        "sizes": ["S", "M", "L", "XL", "2XL"],
        "colors": ["Oxford Grey", "Navy", "Black", "Maroon"],
        "material": "82% Cotton, 18% Polyester",
        "computed": computed(), "created_at": now(),
    },
    {
        "_id": pid(), "type": "clothing",
        "name": "Uniqlo Ultra Light Down Jacket", "price": 5999,
        "category": "Outerwear", "brand": "Uniqlo", "stock_quantity": 70,
        "sizes": ["XS", "S", "M", "L", "XL", "2XL"],
        "colors": ["Black", "Navy", "Olive", "Beige"],
        "material": "100% Nylon shell, 90% Down fill",
        "computed": computed(), "created_at": now(),
    },
]

all_products = electronics + books + clothing
result = products_col.insert_many(all_products)
print(f"✅  Inserted {len(result.inserted_ids)} products")

# ── sample reviews (demonstrates Computed Pattern update) ─────────────────────
sample_reviews = []
ratings_map = {}  # product_id -> list of ratings

review_data = [
    # Electronics
    (all_products[0]["_id"], 5, "Amazing noise cancellation, best headphones I've owned!"),
    (all_products[0]["_id"], 4, "Great sound quality, slightly tight fit after long sessions."),
    (all_products[0]["_id"], 5, "Battery life is incredible. 30 hours is no joke."),
    (all_products[1]["_id"], 5, "Blazing fast, incredible battery life. M3 is a beast."),
    (all_products[1]["_id"], 4, "Excellent machine but pricey. Worth every cent."),
    (all_products[2]["_id"], 4, "Picture quality is stunning. Setup was easy."),
    (all_products[2]["_id"], 3, "Good TV but the smart interface is a bit slow."),
    (all_products[3]["_id"], 5, "Best mouse I've ever used. MagSpeed scroll is magic."),
    (all_products[4]["_id"], 4, "Footage is incredible. HyperSmooth really works."),
    (all_products[5]["_id"], 5, "The M4 chip makes this tablet feel like a laptop."),
    (all_products[6]["_id"], 4, "Great ANC, comfortable fit. Spatial audio is a nice touch."),
    # Books
    (all_products[7]["_id"], 5, "Best programming book ever written. Changed how I code."),
    (all_products[7]["_id"], 5, "Every developer should read this. Timeless advice."),
    (all_products[7]["_id"], 4, "Some examples feel dated but the principles are gold."),
    (all_products[8]["_id"], 5, "Essential reading for every backend engineer."),
    (all_products[8]["_id"], 5, "Dense but incredibly rewarding. Read it twice."),
    (all_products[9]["_id"], 4, "Practical and actionable. Great companion to Clean Code."),
    (all_products[10]["_id"], 4, "Very motivating, practical advice. Easy to read."),
    (all_products[10]["_id"], 5, "Transformed how I approach building habits."),
    (all_products[11]["_id"], 3, "Good reference but a bit dry. Better as a lookup guide."),
    (all_products[12]["_id"], 5, "Perfect intro to Python. Great for beginners."),
    # Clothing
    (all_products[14]["_id"], 5, "Super comfortable, worth every penny. True to size."),
    (all_products[14]["_id"], 4, "Runs slightly small, order a size up."),
    (all_products[15]["_id"], 5, "Classic fit, great denim quality. My go-to jeans."),
    (all_products[16]["_id"], 5, "Incredibly warm and packable. Perfect for travel."),
    (all_products[17]["_id"], 4, "Responsive cushioning. Great for long runs."),
    (all_products[18]["_id"], 5, "Heavyweight feel, great quality for the price."),
    (all_products[19]["_id"], 4, "Lightweight and warm. Packs into its own pocket."),
]

for prod_id, rating, text in review_data:
    sample_reviews.append({
        "_id": ObjectId(),
        "product_id": prod_id,
        "user_id": user_id,
        "rating": rating,
        "text": text,
        "created_at": now(),
    })
    ratings_map.setdefault(str(prod_id), []).append(rating)

reviews_col.insert_many(sample_reviews)
print(f"✅  Inserted {len(sample_reviews)} reviews")

# Update computed fields (Computed Pattern) for reviewed products
for prod_id_str, ratings in ratings_map.items():
    avg = round(sum(ratings) / len(ratings), 2)
    products_col.update_one(
        {"_id": ObjectId(prod_id_str)},
        {"$set": {
            "computed.avg_rating": avg,
            "computed.review_count": len(ratings),
        }}
    )

print("✅  Computed fields updated (avg_rating, review_count)")

# ── demo order (demonstrates $inc on total_sold / total_revenue) ──────────────
order_product = all_products[0]   # Sony headphones
qty = 2
order = {
    "_id": ObjectId(),
    "user_id": user_id,
    "status": "completed",
    "order_items": [
        {
            "product_id": order_product["_id"],
            "name": order_product["name"],
            "price": order_product["price"],   # snapshot at purchase
            "quantity": qty,
            "type": order_product["type"],
        }
    ],
    "total_amount": round(order_product["price"] * qty, 2),
    "created_at": now(),
}
orders_col.insert_one(order)

# Computed Pattern: $inc total_sold and total_revenue
products_col.update_one(
    {"_id": order_product["_id"]},
    {"$inc": {
        "computed.total_sold": qty,
        "computed.total_revenue": order["total_amount"],
        "stock_quantity": -qty,
    }}
)
print(f"✅  Demo order created; computed fields incremented for '{order_product['name']}'")

# ── additional demo orders for monthly revenue report ─────────────────────────
extra_orders = [
    (all_products[7],  3),   # Clean Code x3
    (all_products[14], 2),   # Nike Air Max x2
    (all_products[1],  1),   # MacBook Air x1
    (all_products[10], 4),   # Atomic Habits x4
    (all_products[16], 1),   # Patagonia Jacket x1
]
for prod, q in extra_orders:
    o = {
        "_id": ObjectId(),
        "user_id": user_id,
        "status": "completed",
        "order_items": [{
            "product_id": prod["_id"],
            "name": prod["name"],
            "price": prod["price"],
            "quantity": q,
            "type": prod["type"],
        }],
        "total_amount": round(prod["price"] * q, 2),
        "created_at": now(),
    }
    orders_col.insert_one(o)
    products_col.update_one(
        {"_id": prod["_id"]},
        {"$inc": {
            "computed.total_sold": q,
            "computed.total_revenue": o["total_amount"],
            "stock_quantity": -q,
        }}
    )
print(f"✅  {len(extra_orders)} additional demo orders created")
print("\n🎉  Seed complete. Run `python app.py` to start the API.")
