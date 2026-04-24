/**
 * Shared UI utilities.
 */

// ── Toast notifications ───────────────────────────────────────────────────────
function showToast(message, type = "default", duration = 3000) {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className = "toast-container";
    document.body.appendChild(container);
  }
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), duration);
}

// ── Product type → emoji ──────────────────────────────────────────────────────
function typeEmoji(type) {
  const map = { electronics: "⚡", book: "📚", clothing: "👕" };
  return map[type] || "📦";
}

// ── Star rating ───────────────────────────────────────────────────────────────
function renderStars(rating) {
  const full  = Math.floor(rating);
  const half  = rating - full >= 0.5 ? 1 : 0;
  const empty = 5 - full - half;
  return "★".repeat(full) + (half ? "½" : "") + "☆".repeat(empty);
}

// ── Format currency ───────────────────────────────────────────────────────────
function formatPrice(n) {
  return "₹" + Number(n).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// ── Cart badge ────────────────────────────────────────────────────────────────
async function refreshCartBadge() {
  try {
    const data = await Cart.get();
    const count = data.cart.reduce((s, i) => s + i.qty, 0);
    document.querySelectorAll(".cart-badge").forEach((el) => {
      el.textContent = count;
      el.style.display = count > 0 ? "inline" : "none";
    });
  } catch (_) {}
}

// ── Navbar HTML ───────────────────────────────────────────────────────────────
function renderNavbar(activePage = "") {
  const pages = [
    { href: "index.html",    label: "Catalog" },
    { href: "cart.html",     label: "Cart" },
    { href: "trending.html", label: "Trending" },
    { href: "reports.html",  label: "Reports" },
  ];
  const links = pages
    .map(
      (p) =>
        `<a href="${p.href}" class="${activePage === p.label ? "active" : ""}">${p.label}</a>`
    )
    .join("");

  return `
    <nav class="navbar">
      <a href="index.html" class="logo">Shop<span>Smart</span></a>
      <div class="nav-links">
        ${links}
        <a href="cart.html" class="cart-icon">
          🛒 <span class="cart-badge" style="display:none">0</span>
        </a>
      </div>
    </nav>`;
}
