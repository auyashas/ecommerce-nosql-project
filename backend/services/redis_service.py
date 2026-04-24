"""
Redis service – Shopping Cart, View Counters, Trending, Recently Viewed.
All keys and TTLs follow the spec exactly.

Redis calls are wrapped with try/except so the API degrades gracefully
when Redis is unavailable. Cart falls back to an in-memory store so
add/get/remove all work even without Redis running.
"""
from db import redis_client
from config import (
    CART_TTL_SECONDS,
    VIEW_TTL_SECONDS,
    TRENDING_TTL_SECONDS,
    RECENTLY_VIEWED_MAX,
)

TRENDING_KEY = "trending"

# ── In-memory fallback store (used when Redis is unavailable) ─────────────────
# Structure: { user_id: { product_id: qty } }
_mem_carts: dict = {}
_mem_recently_viewed: dict = {}


def _redis_ok() -> bool:
    """Return True if Redis is reachable."""
    try:
        redis_client.ping()
        return True
    except Exception:
        return False


# ── Cart ──────────────────────────────────────────────────────────────────────

def cart_key(user_id: str) -> str:
    return f"cart:{user_id}"

def cart_add(user_id: str, product_id: str, qty: int) -> None:
    """Add or update quantity in cart hash; reset 24 h TTL."""
    if _redis_ok():
        try:
            key = cart_key(user_id)
            current = int(redis_client.hget(key, product_id) or 0)
            new_qty = current + qty
            if new_qty <= 0:
                redis_client.hdel(key, product_id)
            else:
                redis_client.hset(key, product_id, new_qty)
            redis_client.expire(key, CART_TTL_SECONDS)
            return
        except Exception:
            pass
    # fallback
    cart = _mem_carts.setdefault(user_id, {})
    new_qty = cart.get(product_id, 0) + qty
    if new_qty <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = new_qty

def cart_set(user_id: str, product_id: str, qty: int) -> None:
    """Set exact quantity (0 = remove)."""
    if _redis_ok():
        try:
            key = cart_key(user_id)
            if qty <= 0:
                redis_client.hdel(key, product_id)
            else:
                redis_client.hset(key, product_id, qty)
            redis_client.expire(key, CART_TTL_SECONDS)
            return
        except Exception:
            pass
    # fallback
    cart = _mem_carts.setdefault(user_id, {})
    if qty <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = qty

def cart_remove(user_id: str, product_id: str) -> None:
    if _redis_ok():
        try:
            redis_client.hdel(cart_key(user_id), product_id)
            return
        except Exception:
            pass
    # fallback
    _mem_carts.get(user_id, {}).pop(product_id, None)

def cart_get(user_id: str) -> dict:
    """Return {product_id: qty} dict."""
    if _redis_ok():
        try:
            raw = redis_client.hgetall(cart_key(user_id))
            return {k: int(v) for k, v in raw.items()}
        except Exception:
            pass
    # fallback
    return dict(_mem_carts.get(user_id, {}))

def cart_delete(user_id: str) -> None:
    if _redis_ok():
        try:
            redis_client.delete(cart_key(user_id))
            return
        except Exception:
            pass
    # fallback
    _mem_carts.pop(user_id, None)

def cart_ttl(user_id: str) -> int:
    if _redis_ok():
        try:
            return redis_client.ttl(cart_key(user_id))
        except Exception:
            pass
    return -1

# ── View Counter ──────────────────────────────────────────────────────────────

def view_key(product_id: str) -> str:
    return f"views:{product_id}"

def increment_view(product_id: str) -> int:
    """Increment daily view counter; set 24 h TTL on first hit."""
    try:
        key = view_key(product_id)
        count = redis_client.incr(key)
        if count == 1:                          # first view today
            redis_client.expire(key, VIEW_TTL_SECONDS)
        return count
    except Exception:
        return 0

def get_views(product_id: str) -> int:
    try:
        return int(redis_client.get(view_key(product_id)) or 0)
    except Exception:
        return 0

# ── Trending (Sorted Set) ─────────────────────────────────────────────────────

def trending_increment(product_id: str) -> None:
    """Increment score; set hourly TTL on first increment."""
    try:
        score = redis_client.zincrby(TRENDING_KEY, 1, product_id)
        if score == 1:                          # first hit this hour
            redis_client.expire(TRENDING_KEY, TRENDING_TTL_SECONDS)
    except Exception:
        pass

def get_trending(top_n: int = 10) -> list[dict]:
    """Return list of {product_id, score} sorted descending."""
    try:
        items = redis_client.zrevrange(TRENDING_KEY, 0, top_n - 1, withscores=True)
        return [{"product_id": pid, "score": int(score)} for pid, score in items]
    except Exception:
        return []

def reset_trending() -> None:
    try:
        redis_client.delete(TRENDING_KEY)
    except Exception:
        pass

# ── Recently Viewed (List) ────────────────────────────────────────────────────

def rv_key(user_id: str) -> str:
    return f"recently_viewed:{user_id}"

def push_recently_viewed(user_id: str, product_id: str) -> None:
    """Push to front; remove duplicates; keep last N."""
    if _redis_ok():
        try:
            key = rv_key(user_id)
            redis_client.lrem(key, 0, product_id)
            redis_client.lpush(key, product_id)
            redis_client.ltrim(key, 0, RECENTLY_VIEWED_MAX - 1)
            return
        except Exception:
            pass
    # fallback
    lst = _mem_recently_viewed.setdefault(user_id, [])
    if product_id in lst:
        lst.remove(product_id)
    lst.insert(0, product_id)
    _mem_recently_viewed[user_id] = lst[:RECENTLY_VIEWED_MAX]

def get_recently_viewed(user_id: str) -> list[str]:
    if _redis_ok():
        try:
            return redis_client.lrange(rv_key(user_id), 0, RECENTLY_VIEWED_MAX - 1)
        except Exception:
            pass
    # fallback
    return list(_mem_recently_viewed.get(user_id, []))
