// ===== إعدادات متجر لينا تيك — عدّل هنا =====
const STORE = {
  name: "لينا تيك",
  tagline: "إكسسوارات تقنية فاخرة تواكب أحدث الصيحات",
  currency: "ر.س",
  // رقم واتساب لاستقبال الطلبات (بالصيغة الدولية بدون + أو أصفار بادئة)
  whatsapp: "966500000000",
  email: "hello@linatech.store",
  instagram: "linatech.store",
  shippingFee: 30,
  freeShippingOver: 400,
  cartKey: "linatech_cart",
};

// ===== التصنيفات =====
const CATEGORIES = [
  { id: "all", name: "الكل" },
  { id: "cases", name: "كفرات فاخرة" },
  { id: "charging", name: "الشحن والطاقة" },
  { id: "audio", name: "الصوتيات" },
  { id: "watch", name: "أساور الساعات" },
  { id: "desk", name: "إكسسوارات المكتب" },
  { id: "carry", name: "الحقائب والمحافظ" },
];

// ===== المنتجات — أضف أو احذف أو عدّل =====
// image: رابط صورة (اختياري). إذا تُرك فارغاً تُعرض أيقونة emoji بخلفية ملوّنة.
const PRODUCTS = [
  // كفرات
  { id: 1, name: "كفر جلد طبيعي MagSafe", category: "cases", price: 229, oldPrice: 279, emoji: "📱", color: "#8a5a2b", desc: "جلد إيطالي طبيعي يكتسب لمعة مميزة مع الوقت، مغناطيس MagSafe مدمج وحواف معدنية مطلية.", badge: "الأكثر مبيعاً" },
  { id: 2, name: "كفر ألياف الكربون", category: "cases", price: 189, emoji: "🖤", color: "#3a3a3a", desc: "نحيف جداً بسماكة ٠٫٨ مم من ألياف الأراميد، خفيف الوزن ومقاوم للخدوش." },
  { id: 3, name: "كفر شفاف بإطار ذهبي", category: "cases", price: 149, emoji: "✨", color: "#c9a45c", desc: "تصميم كريستالي لا يصفرّ مع إطار مطلي بلون الذهب الوردي يبرز لون جوالك.", badge: "ترند" },
  // الشحن
  { id: 4, name: "شاحن لاسلكي ٣ في ١", category: "charging", price: 449, oldPrice: 529, emoji: "⚡", color: "#b08d57", desc: "يشحن الجوال والساعة والسماعات معاً بقوة ١٥ واط، قاعدة من الألمنيوم والجلد النباتي.", badge: "خصم" },
  { id: 5, name: "باور بانك مغناطيسي ١٠٠٠٠", category: "charging", price: 259, emoji: "🔋", color: "#5c5c66", desc: "يلتصق بظهر الجوال، شحن سريع ٢٠ واط وشاشة رقمية تعرض نسبة البطارية." },
  { id: 6, name: "كيبل مضفّر فاخر USB-C", category: "charging", price: 79, emoji: "🔌", color: "#7a6a52", desc: "طول ٢ متر، تضفير نايلون متين ورؤوس من الزنك، يدعم شحن حتى ٢٤٠ واط." },
  { id: 7, name: "شاحن جداري GaN ٦٥ واط", category: "charging", price: 199, emoji: "🔆", color: "#4a5a6a", desc: "صغير الحجم بثلاثة منافذ، يشحن اللابتوب والجوال والسماعة في وقت واحد." },
  // الصوتيات
  { id: 8, name: "سماعات لاسلكية بعزل نشط", category: "audio", price: 699, oldPrice: 799, emoji: "🎧", color: "#2f3a4a", desc: "عزل ضوضاء متكيّف، صوت مكاني وبطارية حتى ٣٠ ساعة مع العلبة.", badge: "جديد" },
  { id: 9, name: "علبة جلد للسماعات", category: "audio", price: 119, emoji: "🤎", color: "#6b4630", desc: "جلد مدبوغ نباتياً مع حلقة ذهبية للتعليق، تدعم الشحن اللاسلكي." },
  { id: 10, name: "سماعة بلوتوث محمولة", category: "audio", price: 389, emoji: "🔊", color: "#3d4d44", desc: "صوت ٣٦٠ درجة، مقاومة للماء IP67 وتصميم معدني أنيق." },
  // الساعات
  { id: 11, name: "سوار ستانلس ميلانيز ذهبي", category: "watch", price: 169, emoji: "⌚", color: "#c2a061", desc: "شبك معدني ناعم بإغلاق مغناطيسي، متوافق مع جميع مقاسات Apple Watch.", badge: "ترند" },
  { id: 12, name: "سوار جلد إيطالي", category: "watch", price: 139, emoji: "⌚", color: "#7a3e2e", desc: "جلد طبيعي بخياطة يدوية وإبزيم مطلي، يمنح الساعة طابعاً كلاسيكياً." },
  { id: 13, name: "سوار سيراميك فاخر", category: "watch", price: 249, emoji: "🤍", color: "#9a9a9a", desc: "سيراميك مصقول مقاوم للخدوش، خفيف ولا يتغيّر لونه مع الوقت." },
  // المكتب
  { id: 14, name: "حامل ألمنيوم للجوال", category: "desk", price: 129, emoji: "🗜️", color: "#6e7680", desc: "قطعة ألمنيوم واحدة بزاوية قابلة للتعديل، قاعدة ثقيلة ومانعة للانزلاق." },
  { id: 15, name: "لوح مكتب جلد", category: "desk", price: 179, emoji: "🗂️", color: "#4a3a2a", desc: "مفرش مكتب من الجلد الصناعي الفاخر بوجهين، مقاوم للماء ٩٠×٤٠ سم." },
  { id: 16, name: "تاق تتبّع بحلقة جلد", category: "desk", price: 159, emoji: "📍", color: "#5a4a3a", desc: "اعثر على مفاتيحك وحقيبتك عبر تطبيق Find My، مع حلقة جلد وقطع معدنية ذهبية." },
  // الحقائب
  { id: 17, name: "حقيبة لابتوب جلد", category: "carry", price: 349, oldPrice: 419, emoji: "💼", color: "#5b3a24", desc: "بطانة مخملية واقية وجيب أمامي للشاحن، تناسب الأجهزة حتى ١٤ إنش." },
  { id: 18, name: "منظّم إكسسوارات السفر", category: "carry", price: 159, emoji: "👝", color: "#3e4a40", desc: "جيوب مرنة للكيابل والشواحن والباور بانك، مقاوم للماء وسهل الحمل." },
  { id: 19, name: "محفظة MagSafe جلد", category: "carry", price: 149, emoji: "💳", color: "#7a5230", desc: "تتسع لثلاث بطاقات وتلتصق بقوة بظهر الجوال، مع حماية للبطاقات من التشويش." },
  { id: 20, name: "صندوق هدية لينا تيك", category: "carry", price: 599, oldPrice: 720, emoji: "🎁", color: "#b08d57", desc: "كفر جلد + سوار ساعة + كيبل مضفّر في صندوق أسود فاخر جاهز للإهداء.", badge: "حصري" },
];
