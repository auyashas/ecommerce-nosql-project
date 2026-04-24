from pymongo import MongoClient, ASCENDING, DESCENDING
from redis import Redis
from config import (
    MONGO_URI, MONGO_DB,
    REDIS_HOST, REDIS_PORT, REDIS_DB,
)

# ── MongoDB ──────────────────────────────────────────────────────────────────
_mongo_client = MongoClient(MONGO_URI)
mongo_db = _mongo_client[MONGO_DB]

products_col = mongo_db["products"]
orders_col   = mongo_db["orders"]
reviews_col  = mongo_db["reviews"]
users_col    = mongo_db["users"]

def ensure_indexes():
    # products
    products_col.create_index([("category", ASCENDING)])
    products_col.create_index([("type", ASCENDING)])
    products_col.create_index([("price", ASCENDING)])
    products_col.create_index([("computed.avg_rating", DESCENDING)])
    products_col.create_index([("computed.total_sold", DESCENDING)])
    # orders
    orders_col.create_index([("user_id", ASCENDING)])
    orders_col.create_index([("created_at", DESCENDING)])
    # reviews
    reviews_col.create_index([("product_id", ASCENDING)])
    reviews_col.create_index([("user_id", ASCENDING)])

# ── Redis ─────────────────────────────────────────────────────────────────────
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
