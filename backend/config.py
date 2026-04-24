import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB  = os.getenv("MONGO_DB", "ecommerce")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB   = int(os.getenv("REDIS_DB", 0))

CART_TTL_SECONDS     = 86400   # 24 h – abandoned cart cleanup
VIEW_TTL_SECONDS     = 86400   # 24 h – daily view counter
TRENDING_TTL_SECONDS = 3600    # 1 h  – hourly trending reset
RECENTLY_VIEWED_MAX  = 10      # keep last 10 per user
