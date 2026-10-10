// ===== إعدادات المتجر — عدّل هنا =====
const STORE = {
  name: "تكوين",
  tagline: "منتجات مختارة بعناية، تصلك حتى باب بيتك",
  currency: "ر.س",
  // رقم واتساب لاستقبال الطلبات (بالصيغة الدولية بدون + أو أصفار بادئة)
  whatsapp: "966500000000",
  email: "info@takween.store",
  instagram: "takween.store",
  shippingFee: 25,
  freeShippingOver: 300,
};

// ===== المنتجات — أضف أو احذف أو عدّل =====
// image: رابط صورة (اختياري). إذا تُرك فارغاً تُعرض أيقونة emoji بخلفية ملوّنة.
const CATEGORIES = [
  { id: "all", name: "الكل" },
  { id: "perfume", name: "عطور" },
  { id: "accessories", name: "إكسسوارات" },
  { id: "home", name: "منزل" },
  { id: "gifts", name: "هدايا" },
];

const PRODUCTS = [
  { id: 1, name: "عطر عود ملكي", category: "perfume", price: 249, oldPrice: 299, emoji: "🌹", color: "#7b2d3b", desc: "عطر شرقي فاخر بمزيج العود والورد الطائفي، ثبات يدوم طويلاً.", badge: "الأكثر مبيعاً" },
  { id: 2, name: "دهن مسك أبيض", category: "perfume", price: 89, emoji: "🤍", color: "#8d8a83", desc: "مسك أبيض نقي بملمس ناعم ورائحة نظيفة تناسب الاستخدام اليومي." },
  { id: 3, name: "بخور معطر فاخر", category: "home", price: 65, emoji: "🪔", color: "#a0662b", desc: "قطع بخور مختارة بعناية لتعطير المنزل والمجالس." },
  { id: 4, name: "ساعة جلد كلاسيك", category: "accessories", price: 399, oldPrice: 459, emoji: "⌚", color: "#3f3a35", desc: "ساعة أنيقة بسوار جلد طبيعي ومقاومة للماء.", badge: "خصم" },
  { id: 5, name: "محفظة جلد طبيعي", category: "accessories", price: 149, emoji: "👛", color: "#6b4a2e", desc: "محفظة عملية بتصميم نحيف وجيوب متعددة للبطاقات." },
  { id: 6, name: "شمعة معطرة", category: "home", price: 75, emoji: "🕯️", color: "#c58b4c", desc: "شمعة من شمع الصويا الطبيعي بروائح هادئة تدوم حتى ٤٠ ساعة." },
  { id: 7, name: "صندوق هدية فاخر", category: "gifts", price: 329, emoji: "🎁", color: "#2f4a3e", desc: "تشكيلة مختارة من العطور والبخور في صندوق أنيق جاهز للإهداء.", badge: "جديد" },
  { id: 8, name: "مبخرة نحاسية", category: "home", price: 119, emoji: "🏺", color: "#8a5a24", desc: "مبخرة يدوية الصنع من النحاس بنقوش تراثية." },
  { id: 9, name: "سبحة كهرمان", category: "accessories", price: 189, emoji: "📿", color: "#b5741c", desc: "سبحة من الكهرمان الطبيعي بـ ٣٣ حبة." },
  { id: 10, name: "بطاقة إهداء", category: "gifts", price: 15, emoji: "💌", color: "#9c3d54", desc: "بطاقة بتصميم أنيق مع رسالتك الخاصة تُرفق مع الطلب." },
  { id: 11, name: "معطر مفارش", category: "home", price: 55, emoji: "🌿", color: "#4f6b4a", desc: "رذاذ لطيف لتعطير المفارش والستائر بروائح منعشة." },
  { id: 12, name: "طقم عطور مصغرة", category: "gifts", price: 199, oldPrice: 240, emoji: "✨", color: "#5a4a7b", desc: "خمسة عطور بحجم السفر، مثالية للتجربة والإهداء." },
];
