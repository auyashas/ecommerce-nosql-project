/**
 * API client – thin wrapper around fetch for the Flask backend.
 * Auto-detects base URL: works both when served via Flask (/shop)
 * and when opened directly as a file (falls back to localhost:5000).
 */
const API_BASE = (location.protocol === "file:")
  ? "http://localhost:5000"
  : (location.port === "5000" ? "" : "http://localhost:5000");
// When served by Flask on port 5000, API_BASE is "" (same origin, no prefix needed)

// Persist a simple user ID in localStorage (demo purposes)
function getUserId() {
  let uid = localStorage.getItem("userId");
  if (!uid) {
    uid = "user_" + Math.random().toString(36).slice(2, 10);
    localStorage.setItem("userId", uid);
  }
  return uid;
}

async function apiFetch(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    "X-User-Id": getUserId(),
    ...(options.headers || {}),
  };
  const res = await fetch(API_BASE + path, { ...options, headers });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
}

// ── Products ──────────────────────────────────────────────────────────────────
const Products = {
  list: (params = {}) => {
    const qs = new URLSearchParams(
      Object.fromEntries(Object.entries(params).filter(([, v]) => v !== "" && v != null))
    ).toString();
    return apiFetch(`/products${qs ? "?" + qs : ""}`);
  },
  get: (id) => apiFetch(`/products/${id}`),
};

// ── Cart ──────────────────────────────────────────────────────────────────────
const Cart = {
  get: () => apiFetch("/cart"),
  add: (product_id, qty = 1) =>
    apiFetch("/cart/add", { method: "POST", body: JSON.stringify({ product_id, qty }) }),
  update: (product_id, qty) =>
    apiFetch("/cart/update", { method: "POST", body: JSON.stringify({ product_id, qty }) }),
  remove: (product_id) =>
    apiFetch("/cart/remove", { method: "POST", body: JSON.stringify({ product_id }) }),
};

// ── Checkout ──────────────────────────────────────────────────────────────────
const Checkout = {
  place: () => apiFetch("/checkout", { method: "POST", body: JSON.stringify({}) }),
};

// ── Trending & Recently Viewed ────────────────────────────────────────────────
const Trending = {
  get: () => apiFetch("/trending"),
  recentlyViewed: () => apiFetch("/recently-viewed"),
};

// ── Reports ───────────────────────────────────────────────────────────────────
const Reports = {
  bestSelling: () => apiFetch("/reports/best-selling"),
  bestSellingByCategory: () => apiFetch("/reports/best-selling-by-category"),
  monthlyRevenue: () => apiFetch("/reports/monthly-revenue"),
  lowRated: () => apiFetch("/reports/low-rated"),
  stockSummary: () => apiFetch("/reports/stock-summary"),
};
