(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const CART_KEY = "takween_cart";

  // ---------- Helpers ----------
  const fmt = (n) => `${n.toLocaleString("ar-SA")} ${STORE.currency}`;
  const byId = (id) => PRODUCTS.find((p) => p.id === id);
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

  function thumb(p) {
    const bg = `background: linear-gradient(135deg, ${p.color}22, ${p.color}55)`;
    const inner = p.image ? `<img src="${esc(p.image)}" alt="${esc(p.name)}" loading="lazy" />` : p.emoji;
    return { bg, inner };
  }

  function loadCart() {
    try {
      const raw = JSON.parse(localStorage.getItem(CART_KEY) || "{}");
      // تجاهل المنتجات التي حُذفت من الكتالوج
      return Object.fromEntries(Object.entries(raw).filter(([id, q]) => byId(+id) && q > 0));
    } catch {
      return {};
    }
  }
  function saveCart() {
    try { localStorage.setItem(CART_KEY, JSON.stringify(state.cart)); } catch {}
  }

  function toast(msg) {
    const t = $("#toast");
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(toast._t);
    toast._t = setTimeout(() => t.classList.remove("show"), 1800);
  }

  const state = {
    category: "all",
    query: "",
    cart: loadCart(),
  };

  // ---------- Store info ----------
  function renderStoreInfo() {
    document.title = `${STORE.name} | المتجر`;
    document.querySelectorAll("[data-store-name]").forEach((el) => (el.textContent = STORE.name));
    document.querySelectorAll("[data-store-tagline]").forEach((el) => (el.textContent = STORE.tagline));
    $("#shipNote").textContent = STORE.freeShippingOver
      ? `مجاني للطلبات فوق ${fmt(STORE.freeShippingOver)}`
      : `رسوم الشحن ${fmt(STORE.shippingFee)}`;
    $("#year").textContent = new Date().getFullYear();

    const links = [];
    if (STORE.whatsapp) links.push(`<a href="https://wa.me/${STORE.whatsapp}" target="_blank" rel="noopener">واتساب</a>`);
    if (STORE.instagram) links.push(`<a href="https://instagram.com/${esc(STORE.instagram)}" target="_blank" rel="noopener">إنستغرام</a>`);
    if (STORE.email) links.push(`<a href="mailto:${esc(STORE.email)}">البريد</a>`);
    $("#contactLinks").innerHTML = links.join("");
  }

  // ---------- Catalog ----------
  function renderCats() {
    $("#cats").innerHTML = CATEGORIES.map(
      (c) => `<button class="cat ${c.id === state.category ? "active" : ""}" data-cat="${c.id}">${esc(c.name)}</button>`
    ).join("");
  }

  function renderGrid() {
    const q = state.query.trim().toLowerCase();
    const list = PRODUCTS.filter(
      (p) =>
        (state.category === "all" || p.category === state.category) &&
        (!q || p.name.toLowerCase().includes(q) || p.desc.toLowerCase().includes(q))
    );
    $("#empty").hidden = list.length > 0;
    $("#grid").innerHTML = list
      .map((p) => {
        const t = thumb(p);
        return `
        <article class="card">
          <div class="thumb" style="${t.bg}" data-view="${p.id}">
            ${t.inner}
            ${p.badge ? `<span class="badge">${esc(p.badge)}</span>` : ""}
          </div>
          <div class="card__body">
            <div class="card__title" data-view="${p.id}">${esc(p.name)}</div>
            <div class="price"><b>${fmt(p.price)}</b>${p.oldPrice ? `<s>${fmt(p.oldPrice)}</s>` : ""}</div>
            <button class="btn btn--primary" data-add="${p.id}">أضف للسلة</button>
          </div>
        </article>`;
      })
      .join("");
  }

  function openProduct(id) {
    const p = byId(id);
    const t = thumb(p);
    $("#productModalBody").innerHTML = `
      <div class="pm__thumb" style="${t.bg}">${t.inner}</div>
      <h3>${esc(p.name)}</h3>
      <div class="price"><b>${fmt(p.price)}</b>${p.oldPrice ? `<s>${fmt(p.oldPrice)}</s>` : ""}</div>
      <p class="pm__desc">${esc(p.desc)}</p>
      <div class="pm__row">
        <div class="qty"><button data-pm="-1">−</button><span id="pmQty">1</span><button data-pm="1">+</button></div>
        <button class="btn btn--primary" data-pm-add="${p.id}">أضف للسلة</button>
      </div>`;
    open("#productModal");
  }

  // ---------- Cart ----------
  const cartEntries = () => Object.entries(state.cart).map(([id, qty]) => ({ p: byId(+id), qty }));
  const cartCount = () => Object.values(state.cart).reduce((a, b) => a + b, 0);

  function totals() {
    const subtotal = cartEntries().reduce((s, { p, qty }) => s + p.price * qty, 0);
    const free = STORE.freeShippingOver && subtotal >= STORE.freeShippingOver;
    const shipping = subtotal === 0 || free ? 0 : STORE.shippingFee;
    return { subtotal, shipping, total: subtotal + shipping };
  }

  function addToCart(id, qty = 1) {
    state.cart[id] = (state.cart[id] || 0) + qty;
    saveCart();
    renderCart();
    const c = $("#cartCount");
    c.classList.remove("bump"); void c.offsetWidth; c.classList.add("bump");
    toast(`تمت إضافة "${byId(id).name}" إلى السلة`);
  }

  function setQty(id, qty) {
    if (qty <= 0) delete state.cart[id];
    else state.cart[id] = qty;
    saveCart();
    renderCart();
  }

  function summaryHtml() {
    const { subtotal, shipping, total } = totals();
    let note = "";
    if (STORE.freeShippingOver && subtotal > 0 && subtotal < STORE.freeShippingOver) {
      note = `<div class="muted">أضف ${fmt(STORE.freeShippingOver - subtotal)} للحصول على شحن مجاني</div>`;
    }
    return `
      <div class="row"><span>المجموع الفرعي</span><span>${fmt(subtotal)}</span></div>
      <div class="row"><span>الشحن</span><span>${shipping ? fmt(shipping) : "مجاني"}</span></div>
      <div class="row row--total"><span>الإجمالي</span><span>${fmt(total)}</span></div>
      ${note}`;
  }

  function renderCart() {
    $("#cartCount").textContent = cartCount();
    const items = cartEntries();
    if (!items.length) {
      $("#cartItems").innerHTML = `<div class="cart-empty"><span>🛒</span>سلتك فارغة</div>`;
      $("#cartFoot").innerHTML = "";
      return;
    }
    $("#cartItems").innerHTML = items
      .map(({ p, qty }) => {
        const t = thumb(p);
        return `
        <div class="ci">
          <div class="ci__thumb" style="${t.bg}">${t.inner}</div>
          <div class="ci__info"><b>${esc(p.name)}</b><small>${fmt(p.price)}</small></div>
          <div class="qty">
            <button data-qty="${p.id}" data-d="-1">−</button><span>${qty}</span><button data-qty="${p.id}" data-d="1">+</button>
          </div>
        </div>`;
      })
      .join("");
    $("#cartFoot").innerHTML = `${summaryHtml()}<button class="btn btn--primary btn--block" id="toCheckout">إتمام الطلب</button>`;
  }

  // ---------- Checkout ----------
  function submitOrder(e) {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(e.target));
    const { subtotal, shipping, total } = totals();
    const lines = cartEntries().map(({ p, qty }) => `• ${p.name} × ${qty} = ${fmt(p.price * qty)}`);
    const msg = [
      `طلب جديد من متجر ${STORE.name} 🛍️`,
      "",
      ...lines,
      "",
      `المجموع: ${fmt(subtotal)}`,
      `الشحن: ${shipping ? fmt(shipping) : "مجاني"}`,
      `الإجمالي: ${fmt(total)}`,
      "",
      `الاسم: ${f.name}`,
      `الجوال: ${f.phone}`,
      `المدينة: ${f.city}`,
      `العنوان: ${f.address}`,
      f.notes ? `ملاحظات: ${f.notes}` : "",
    ].filter((l, i, a) => l !== "" || a[i - 1] !== "").join("\n");

    window.open(`https://wa.me/${STORE.whatsapp}?text=${encodeURIComponent(msg)}`, "_blank");
    state.cart = {};
    saveCart();
    renderCart();
    e.target.reset();
    closeAll();
    toast("شكراً لك! تم تحويلك إلى واتساب لتأكيد الطلب");
  }

  // ---------- Overlays ----------
  function open(sel) {
    closeAll();
    $(sel).hidden = false;
    document.body.style.overflow = "hidden";
  }
  function closeAll() {
    document.querySelectorAll(".modal, .drawer").forEach((m) => (m.hidden = true));
    document.body.style.overflow = "";
  }

  // ---------- Events ----------
  document.addEventListener("click", (e) => {
    const t = e.target.closest("button, [data-view], [data-close]");
    if (!t) return;
    const d = t.dataset;
    if (d.close !== undefined) return closeAll();
    if (d.cat) { state.category = d.cat; renderCats(); renderGrid(); return; }
    if (d.view) return openProduct(+d.view);
    if (d.add) return addToCart(+d.add);
    if (d.qty) return setQty(+d.qty, (state.cart[d.qty] || 0) + +d.d);
    if (d.pm) {
      const el = $("#pmQty");
      el.textContent = Math.max(1, +el.textContent + +d.pm);
      return;
    }
    if (d.pmAdd) { addToCart(+d.pmAdd, +$("#pmQty").textContent); return closeAll(); }
    if (t.id === "openCart") return open("#cartDrawer");
    if (t.id === "toCheckout") {
      $("#checkoutSummary").innerHTML = summaryHtml();
      return open("#checkoutModal");
    }
  });
  document.addEventListener("keydown", (e) => e.key === "Escape" && closeAll());
  $("#search").addEventListener("input", (e) => { state.query = e.target.value; renderGrid(); });
  $("#checkoutForm").addEventListener("submit", submitOrder);

  // ---------- Init ----------
  renderStoreInfo();
  renderCats();
  renderGrid();
  renderCart();
})();
