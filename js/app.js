(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  // ---------- Helpers ----------
  const fmt = (n) => `${Math.round(n).toLocaleString("ar-SA")} ${STORE.currency}`;
  const byId = (id) => PRODUCTS.find((p) => p.id === id);
  const catName = (id) => (CATEGORIES.find((c) => c.id === id) || {}).name || "";
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const waLink = (text) => `https://wa.me/${STORE.whatsapp}${text ? `?text=${encodeURIComponent(text)}` : ""}`;
  const mem = {
    get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
  };

  function svg(name) {
    const body = (typeof ICONS !== "undefined" && ICONS[name]) || "";
    return `<svg viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${body}</svg>`;
  }
  function art(p, cls = "art") {
    const inner = p.image ? `<img src="${esc(p.image)}" alt="${esc(p.name)}" decoding="async" />` : svg(p.icon);
    return `<div class="${cls}">${inner}</div>`;
  }
  const priceHtml = (p) =>
    `<div class="price"><b>${fmt(p.price)}</b>${p.oldPrice ? `<s>${fmt(p.oldPrice)}</s><em>وفّر ${Math.round((1 - p.price / p.oldPrice) * 100)}٪</em>` : ""}</div>`;

  function toast(msg) {
    const t = $("#toast");
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(toast._t);
    toast._t = setTimeout(() => t.classList.remove("show"), 2000);
  }

  // ---------- State ----------
  const saved = mem.get(STORE.cartKey, {});
  const state = {
    cat: "all",
    q: "",
    sort: "featured",
    cart: (Array.isArray(saved.lines) ? saved.lines : []).filter((l) => byId(l.id) && l.qty > 0),
    coupon: COUPONS[saved.coupon] ? saved.coupon : "",
    modal: null, // { id, finish, qty }
  };
  const save = () => mem.set(STORE.cartKey, { lines: state.cart, coupon: state.coupon });

  // ---------- Store info ----------
  function renderInfo() {
    document.title = `${STORE.name} | ${STORE.tagline}`;
    $$("[data-store-name]").forEach((el) => (el.textContent = STORE.name));
    $$("[data-store-name-en]").forEach((el) => (el.textContent = STORE.nameEn));
    $$("[data-store-tagline]").forEach((el) => (el.textContent = STORE.tagline));
    $$("[data-free-over]").forEach((el) => (el.textContent = fmt(STORE.freeShippingOver)));
    $$("[data-ship-days]").forEach((el) => (el.textContent = STORE.shippingDays));
    $$("[data-wa]").forEach((el) => (el.href = waLink("مرحباً لينا تيك، عندي استفسار")));
    $("#year").textContent = new Date().getFullYear();
    $("#contactList").innerHTML = `
      <li><span>واتساب</span><a href="${waLink()}" target="_blank" rel="noopener" dir="ltr">+${esc(STORE.whatsapp)}</a></li>
      <li><span>البريد</span><span class="sel" dir="ltr">${esc(STORE.email)}</span></li>
      <li><span>إنستغرام</span><a href="https://instagram.com/${esc(STORE.instagram)}" target="_blank" rel="noopener" dir="ltr">@${esc(STORE.instagram)}</a></li>
      <li><span>تيك توك</span><a href="https://www.tiktok.com/@${esc(STORE.tiktok)}" target="_blank" rel="noopener" dir="ltr">@${esc(STORE.tiktok)}</a></li>
      <li><span>الموقع</span><span>${esc(STORE.city)}</span></li>`;
    $("#payments").innerHTML = STORE.payments.map((p) => `<span>${esc(p)}</span>`).join("");
    $("#footCats").innerHTML = CATEGORIES.filter((c) => c.id !== "all")
      .map((c) => `<li><a href="#products" data-act="cat" data-cat="${c.id}">${esc(c.name)}</a></li>`).join("");
  }

  // ---------- Category nav + new arrivals ----------
  function renderCatNav() {
    $("#catNav").innerHTML = CATEGORIES.filter((c) => c.id !== "all")
      .map((c) => `<a href="#products" class="catnav__item" data-act="cat" data-cat="${c.id}">
          <span class="catnav__img"><img src="${esc(c.image)}" alt="" loading="lazy" /></span>
          <span>${esc(c.name)}</span>
        </a>`).join("");
  }

  function renderNew() {
    $("#newRow").innerHTML = PRODUCTS.filter((p) => p.isNew).map((p) => `
      <article class="tile">
        <button type="button" class="tile__btn" data-act="view" data-id="${p.id}">
          <span class="tile__txt">
            <small class="tile__eyebrow">${esc(p.badge || "جديد")}</small>
            <b>${esc(p.name)}</b>
            <span class="tile__desc">${esc(p.desc)}</span>
            <span class="tile__price">${fmt(p.price)}</span>
          </span>
          ${art(p, "art art--tile")}
        </button>
      </article>`).join("");
  }

  function renderStatic() {
    $("#faqList").innerHTML = FAQ.map(
      (f, i) => `<details${i === 0 ? " open" : ""}><summary>${esc(f.q)}</summary><p>${esc(f.a)}</p></details>`
    ).join("");
  }

  // ---------- Catalog ----------
  function renderCats() {
    $("#cats").innerHTML = CATEGORIES.map(
      (c) => `<button type="button" class="chip ${c.id === state.cat ? "active" : ""}" data-act="cat" data-cat="${c.id}">${esc(c.name)}</button>`
    ).join("");
  }

  function list() {
    const q = state.q.trim().toLowerCase();
    const items = PRODUCTS.filter(
      (p) => (state.cat === "all" || p.category === state.cat) &&
        (!q || [p.name, p.desc, catName(p.category)].some((s) => s.toLowerCase().includes(q)))
    );
    const sorters = {
      featured: (a, b) => a.rank - b.rank,
      new: (a, b) => (b.badge === "جديد") - (a.badge === "جديد") || b.id - a.id,
      low: (a, b) => a.price - b.price,
      high: (a, b) => b.price - a.price,
    };
    return items.sort(sorters[state.sort]);
  }

  function renderGrid() {
    const items = list();
    $("#empty").hidden = items.length > 0;
    $("#resultCount").textContent = `${items.length.toLocaleString("ar-SA")} منتج`;
    $("#grid").innerHTML = items.map((p) => `
      <article class="card">
        <button type="button" class="card__media" data-act="view" data-id="${p.id}" aria-label="عرض ${esc(p.name)}">
          ${art(p)}
          ${p.badge ? `<span class="badge">${esc(p.badge)}</span>` : ""}
        </button>
        <div class="card__body">
          <small class="card__cat">${esc(catName(p.category))}</small>
          <h3 class="card__title"><button type="button" data-act="view" data-id="${p.id}">${esc(p.name)}</button></h3>
          ${priceHtml(p)}
          <button type="button" class="btn btn--buy" data-act="quick" data-id="${p.id}">أضيفي للسلة</button>
        </div>
      </article>`).join("");
  }

  // ---------- Product modal ----------
  function openProduct(id) {
    const p = byId(id);
    state.modal = { id, finish: (p.finishes || [])[0] || "", qty: 1 };
    renderProduct();
    open("#productModal");
  }
  function renderProduct() {
    const p = byId(state.modal.id);
    const m = state.modal;
    $("#productModalBody").innerHTML = `
      <div class="pm">
        <div class="pm__media">${art(p, "art art--lg")}${p.badge ? `<span class="badge">${esc(p.badge)}</span>` : ""}</div>
        <div class="pm__info">
          <small class="card__cat">${esc(catName(p.category))}</small>
          <h3 id="pmTitle">${esc(p.name)}</h3>
          ${priceHtml(p)}
          <p class="pm__desc">${esc(p.desc)}</p>
          ${p.finishes?.length ? `
            <div class="pm__opt">
              <span>الخيار: <b>${esc(m.finish)}</b></span>
              <div class="opts">${p.finishes.map((f) => `<button type="button" class="opt ${f === m.finish ? "active" : ""}" data-act="finish" data-v="${esc(f)}">${esc(f)}</button>`).join("")}</div>
            </div>` : ""}
          <ul class="specs">${(p.specs || []).map((s) => `<li>${esc(s)}</li>`).join("")}</ul>
          <div class="pm__row">
            <div class="qty"><button type="button" data-act="pmqty" data-d="1" aria-label="زيادة">+</button><span>${m.qty.toLocaleString("ar-SA")}</span><button type="button" data-act="pmqty" data-d="-1" aria-label="إنقاص">−</button></div>
            <button type="button" class="btn btn--primary" data-act="pmadd">أضيفي للسلة · ${fmt(p.price * m.qty)}</button>
          </div>
          <p class="pm__note">شحن ${esc(STORE.shippingDays)} · استبدال خلال ١٤ يوماً</p>
        </div>
      </div>`;
  }

  // ---------- Cart ----------
  const lineKey = (l) => `${l.id}|${l.finish}`;
  const count = () => state.cart.reduce((a, l) => a + l.qty, 0);

  function totals() {
    const subtotal = state.cart.reduce((s, l) => s + byId(l.id).price * l.qty, 0);
    const c = COUPONS[state.coupon];
    const discount = c ? Math.round((subtotal * c.pct) / 100) : 0;
    const net = subtotal - discount;
    const shipping = subtotal === 0 || net >= STORE.freeShippingOver ? 0 : STORE.shippingFee;
    return { subtotal, discount, net, shipping, total: net + shipping };
  }

  function addToCart(id, finish, qty = 1) {
    const p = byId(id);
    finish = finish ?? ((p.finishes || [])[0] || "");
    const line = state.cart.find((l) => l.id === id && l.finish === finish);
    if (line) line.qty += qty;
    else state.cart.push({ id, finish, qty });
    save();
    renderCart();
    const c = $("#cartCount");
    c.classList.remove("bump"); void c.offsetWidth; c.classList.add("bump");
    toast(`أُضيف «${p.name}» إلى السلة`);
  }

  function summaryHtml() {
    const t = totals();
    return `
      <div class="row"><span>المجموع الفرعي</span><span>${fmt(t.subtotal)}</span></div>
      ${t.discount ? `<div class="row row--gold"><span>خصم ${esc(state.coupon)}</span><span>− ${fmt(t.discount)}</span></div>` : ""}
      <div class="row"><span>الشحن</span><span>${t.shipping ? fmt(t.shipping) : "مجاني"}</span></div>
      <div class="row row--total"><span>الإجمالي</span><span>${fmt(t.total)}</span></div>`;
  }

  function renderCart() {
    $("#cartCount").textContent = count().toLocaleString("ar-SA");
    $("#cartCount").hidden = count() === 0;
    $("#cartTitleCount").textContent = count() ? `(${count().toLocaleString("ar-SA")})` : "";
    if (!state.cart.length) {
      $("#cartItems").innerHTML = `<div class="cart-empty"><img src="images/gift-box.webp" alt="" /><p>سلتك فارغة حالياً</p><button type="button" class="btn btn--line" data-close>تصفّحي المتجر</button></div>`;
      $("#cartFoot").innerHTML = "";
      return;
    }
    const t = totals();
    const left = STORE.freeShippingOver - t.net;
    const pct = Math.min(100, (t.net / STORE.freeShippingOver) * 100);
    $("#cartItems").innerHTML = `
      <div class="ship">
        <p>${left > 0 ? `أضيفي <b>${fmt(left)}</b> وتحصلين على شحن مجاني` : "مبروك! طلبك مؤهّل للشحن المجاني"}</p>
        <div class="ship__bar"><span style="width:${pct}%"></span></div>
      </div>
      ${state.cart.map((l) => {
        const p = byId(l.id);
        return `
        <div class="ci">
          ${art(p, "art art--sm")}
          <div class="ci__info">
            <b>${esc(p.name)}</b>
            ${l.finish ? `<small>${esc(l.finish)}</small>` : ""}
            <span class="ci__price">${fmt(p.price * l.qty)}</span>
          </div>
          <div class="ci__ctl">
            <div class="qty qty--sm"><button type="button" data-act="qty" data-k="${esc(lineKey(l))}" data-d="1" aria-label="زيادة">+</button><span>${l.qty.toLocaleString("ar-SA")}</span><button type="button" data-act="qty" data-k="${esc(lineKey(l))}" data-d="-1" aria-label="إنقاص">−</button></div>
            <button type="button" class="link" data-act="remove" data-k="${esc(lineKey(l))}">إزالة</button>
          </div>
        </div>`;
      }).join("")}`;
    const c = COUPONS[state.coupon];
    $("#cartFoot").innerHTML = `
      <form class="coupon" id="couponForm">
        <label class="sr" for="couponInput">كود الخصم</label>
        <input id="couponInput" name="code" placeholder="كود الخصم" autocomplete="off" dir="ltr" value="${esc(state.coupon)}" />
        <button type="submit" class="btn btn--line">${c ? "تغيير" : "تطبيق"}</button>
      </form>
      ${c ? `<p class="coupon__ok">✓ ${esc(c.label)} <button type="button" class="link" data-act="uncoupon">إلغاء</button></p>` : `<p class="coupon__hint">جرّب الكود <b dir="ltr">LINA10</b> لخصم أول طلب</p>`}
      ${summaryHtml()}
      <button type="button" class="btn btn--primary btn--block" data-act="checkout">إتمام الطلب</button>`;
  }

  function setQty(key, d) {
    const l = state.cart.find((x) => lineKey(x) === key);
    if (!l) return;
    l.qty += d;
    if (l.qty <= 0) state.cart = state.cart.filter((x) => x !== l);
    save();
    renderCart();
  }

  // ---------- Checkout ----------
  function startCheckout() {
    $("#checkoutForm").hidden = false;
    $("#orderDone").hidden = true;
    $("#checkoutSummary").innerHTML = summaryHtml();
    open("#checkoutModal");
  }

  function submitOrder(e) {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(e.target));
    const t = totals();
    const orderNo = `LT-${Date.now().toString().slice(-6)}`;
    const lines = state.cart.map((l) => {
      const p = byId(l.id);
      return `• ${p.name}${l.finish ? ` (${l.finish})` : ""} × ${l.qty} = ${fmt(p.price * l.qty)}`;
    });
    const msg = [
      `طلب جديد من متجر ${STORE.name} ✦`,
      `رقم الطلب: ${orderNo}`,
      "",
      ...lines,
      "",
      `المجموع: ${fmt(t.subtotal)}`,
      t.discount ? `الخصم (${state.coupon}): −${fmt(t.discount)}` : null,
      `الشحن: ${t.shipping ? fmt(t.shipping) : "مجاني"}`,
      `الإجمالي: ${fmt(t.total)}`,
      "",
      `الاسم: ${f.name}`,
      `الجوال: ${f.phone}`,
      `المدينة: ${f.city}`,
      `العنوان: ${f.address}`,
      `طريقة الدفع: ${f.payment}`,
      f.notes ? `ملاحظات: ${f.notes}` : null,
    ].filter((l) => l !== null).join("\n");

    $("#orderNo").textContent = orderNo;
    $("#orderText").textContent = msg;
    $("#sendWa").href = waLink(msg);
    $("#checkoutForm").hidden = true;
    $("#orderDone").hidden = false;
  }

  function finishOrder() {
    state.cart = [];
    state.coupon = "";
    save();
    renderCart();
    $("#checkoutForm").reset();
    setTimeout(() => { closeAll(); toast("شكراً لك! سنؤكد طلبك على واتساب"); }, 300);
  }

  function copyOrder() {
    const text = $("#orderText").textContent;
    const fallback = () => {
      const r = document.createRange();
      r.selectNodeContents($("#orderText"));
      const s = getSelection(); s.removeAllRanges(); s.addRange(r);
      toast("حدّدنا نص الطلب، انسخه يدوياً");
    };
    try {
      navigator.clipboard.writeText(text).then(() => toast("تم نسخ تفاصيل الطلب"), fallback);
    } catch { fallback(); }
  }

  // ---------- Overlays ----------
  let lastFocus = null;
  function open(sel) {
    closeAll(true);
    lastFocus = document.activeElement;
    const el = $(sel);
    el.hidden = false;
    document.body.classList.add("locked");
    setTimeout(() => (el.querySelector("[data-autofocus], button, input") || el).focus(), 30);
  }
  function closeAll(silent) {
    $$(".modal, .drawer").forEach((m) => (m.hidden = true));
    document.body.classList.remove("locked");
    if (!silent && lastFocus) lastFocus.focus?.();
  }

  // ---------- Events ----------
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-close]")) return closeAll();
    const t = e.target.closest("[data-act]");
    if (!t) return;
    const d = t.dataset;
    switch (d.act) {
      case "cat":
        state.cat = d.cat;
        renderCats(); renderGrid();
        if (t.tagName === "A") { e.preventDefault(); closeAll(true); $("#products").scrollIntoView({ behavior: "smooth" }); }
        break;
      case "view": return openProduct(+d.id);
      case "quick": return addToCart(+d.id);
      case "finish": state.modal.finish = d.v; return renderProduct();
      case "pmqty": state.modal.qty = Math.max(1, state.modal.qty + +d.d); return renderProduct();
      case "pmadd": addToCart(state.modal.id, state.modal.finish, state.modal.qty); return closeAll();
      case "qty": return setQty(d.k, +d.d);
      case "remove": return setQty(d.k, -Infinity);
      case "uncoupon": state.coupon = ""; save(); return renderCart();
      case "cart": return open("#cartDrawer");
      case "checkout": return startCheckout();
      case "copy": return copyOrder();
      case "sent": return finishOrder();
    }
  });

  document.addEventListener("submit", (e) => {
    if (e.target.id === "couponForm") {
      e.preventDefault();
      const code = (e.target.code.value || "").trim().toUpperCase();
      if (!code) return;
      if (COUPONS[code]) { state.coupon = code; save(); renderCart(); toast(`تم تطبيق ${COUPONS[code].label}`); }
      else toast("الكود غير صحيح، تأكد منه وحاول مرة أخرى");
    }
  });

  document.addEventListener("keydown", (e) => e.key === "Escape" && closeAll());
  $("#search").addEventListener("input", (e) => { state.q = e.target.value; renderGrid(); });
  $("#sort").addEventListener("change", (e) => { state.sort = e.target.value; renderGrid(); });
  $("#checkoutForm").addEventListener("submit", submitOrder);

  // ---------- Init ----------
  renderInfo();
  renderStatic();
  renderCatNav();
  renderNew();
  renderCats();
  renderGrid();
  renderCart();
})();
