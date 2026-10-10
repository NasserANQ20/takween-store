// رسومات خطية للمنتجات (viewBox 120×120) — تُلوَّن باللون الذهبي من CSS
const ICONS = (() => {
  const phone = `<rect x="38" y="16" width="44" height="88" rx="11"/>`;
  const watchBody = `<rect x="42" y="40" width="36" height="42" rx="11"/><rect x="47" y="45" width="26" height="32" rx="7" opacity=".45"/><path d="M78 54h4v8h-4"/>`;
  return {
    case: `${phone}<rect x="44" y="23" width="20" height="20" rx="6"/><circle cx="50" cy="29" r="2.6"/><circle cx="58" cy="37" r="2.6"/><circle cx="60" cy="68" r="13" opacity=".55"/><circle cx="60" cy="68" r="2" />`,
    carbon: `${phone}<rect x="44" y="23" width="20" height="20" rx="6"/><path d="M44 58l32-14M44 70l32-14M44 82l32-14M44 94l32-14" opacity=".5"/>`,
    clear: `${phone}<rect x="43" y="21" width="34" height="78" rx="8" opacity=".4"/><rect x="47" y="26" width="16" height="16" rx="5"/><path d="M92 26v10M87 31h10M28 80v8M24 84h8" />`,
    charger3: `<path d="M18 92h84a6 6 0 0 1 0 12H18a6 6 0 0 1 0-12z"/><path d="M38 92V40l8-18"/><rect x="40" y="14" width="26" height="46" rx="7" transform="rotate(12 53 37)"/><rect x="68" y="66" width="18" height="22" rx="6"/><path d="M71 66v-6h12v6M71 88v4h12v-4"/><rect x="90" y="78" width="12" height="14" rx="6"/>`,
    powerbank: `<rect x="34" y="18" width="52" height="84" rx="14"/><path d="M64 38L52 60h14L54 82"/><path d="M46 94h4M56 94h4M66 94h4" />`,
    cable: `<rect x="14" y="20" width="14" height="24" rx="4"/><path d="M18 20v-7M24 20v-7"/><path d="M21 44c0 26 18 18 34 34s18 26 40 12"/><rect x="92" y="74" width="22" height="13" rx="4" transform="rotate(-30 103 80)"/>`,
    wall: `<rect x="32" y="30" width="56" height="62" rx="12"/><path d="M48 30V16M72 30V16"/><rect x="44" y="50" width="12" height="6" rx="2"/><rect x="64" y="50" width="12" height="6" rx="2"/><rect x="52" y="70" width="16" height="7" rx="1.5"/>`,
    headphones: `<path d="M24 74V62a36 36 0 0 1 72 0v12"/><rect x="16" y="66" width="20" height="36" rx="9"/><rect x="84" y="66" width="20" height="36" rx="9"/><path d="M36 76h4v18h-4M84 76h-4v18h4" opacity=".6"/>`,
    earcase: `<rect x="28" y="40" width="64" height="56" rx="24"/><path d="M28 62h64" /><circle cx="60" cy="74" r="2.4"/><circle cx="60" cy="26" r="12"/><path d="M60 38v2"/>`,
    speaker: `<rect x="36" y="14" width="48" height="92" rx="24"/><circle cx="60" cy="66" r="16"/><circle cx="60" cy="66" r="6" opacity=".6"/><path d="M52 32h16" /><path d="M54 92h12" opacity=".6"/>`,
    watchMesh: `${watchBody}<path d="M46 40V12h28v28M46 82v26h28V82"/><path d="M46 18h28M46 24h28M46 30h28M46 88h28M46 94h28M46 100h28" opacity=".45"/>`,
    watchLeather: `${watchBody}<path d="M47 40l2-28h22l2 28M47 82l2 26h22l2-26"/><circle cx="60" cy="94" r="1.8"/><circle cx="60" cy="101" r="1.8"/><rect x="52" y="20" width="16" height="6" rx="2" opacity=".6"/>`,
    watchCeramic: `${watchBody}<path d="M47 40V12h26v28M47 82v26h26V82"/><path d="M47 21h26M47 30h26M47 91h26M47 100h26M60 12v28M60 82v26" opacity=".45"/>`,
    stand: `<path d="M30 102h60"/><path d="M40 102l18-40"/><path d="M58 62L44 20"/><rect x="44" y="12" width="34" height="58" rx="8" transform="rotate(-18 61 41)"/><path d="M66 102L58 62" opacity=".5"/>`,
    deskmat: `<path d="M14 82l22-38h70l-22 38z"/><path d="M22 78l17-30h58l-17 30z" stroke-dasharray="3 4" opacity=".55"/><rect x="46" y="54" width="24" height="16" rx="3" opacity=".7"/>`,
    tag: `<circle cx="60" cy="76" r="26"/><circle cx="60" cy="76" r="17" opacity=".45"/><path d="M50 52V26a10 10 0 0 1 20 0v26"/><circle cx="60" cy="24" r="3"/>`,
    bag: `<rect x="16" y="40" width="88" height="62" rx="9"/><path d="M46 40V30a6 6 0 0 1 6-6h16a6 6 0 0 1 6 6v10"/><path d="M16 62h88" opacity=".5"/><rect x="54" y="57" width="12" height="10" rx="2"/>`,
    pouch: `<path d="M18 50c0-10 8-14 18-14h48c10 0 18 4 18 14v30c0 12-8 18-18 18H36c-10 0-18-6-18-18z"/><path d="M22 50h76"/><path d="M84 50v12" /><circle cx="84" cy="66" r="4"/><path d="M34 70h18M34 80h12" opacity=".5"/>`,
    wallet: `<rect x="26" y="36" width="68" height="62" rx="10"/><path d="M34 36V26h52v10" opacity=".55"/><path d="M30 30v-8h44v8" opacity=".35"/><path d="M26 56h68"/><circle cx="60" cy="78" r="9" opacity=".55"/>`,
    gift: `<rect x="20" y="48" width="80" height="54" rx="6"/><rect x="14" y="36" width="92" height="14" rx="4"/><path d="M60 36v66"/><path d="M60 36c-6-14-26-18-26-6 0 6 12 6 26 6zM60 36c6-14 26-18 26-6 0 6-12 6-26 6z"/>`,
  };
})();
