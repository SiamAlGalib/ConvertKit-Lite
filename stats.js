import { db, rtdb } from "/blog/firebase.js";
import { doc, setDoc, increment } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";
import { ref, push, set, onValue, onDisconnect } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-database.js";

export function trackPresence() {
  try {
    const me = push(ref(rtdb, "presence"));
    onValue(ref(rtdb, ".info/connected"), s => {
      if (s.val() === true) {
        onDisconnect(me).remove();
        set(me, { page: location.pathname, t: Date.now() });
      }
    });
  } catch (e) {}
}

/* ---------- country lookup for clicks (once per browser session) ---------- */
let ccPromise = null;
function getCountry() {
  if (ccPromise) return ccPromise;
  try {
    const cached = sessionStorage.getItem("ckl_click_cc");
    if (cached) return (ccPromise = Promise.resolve(cached));
  } catch (e) {}
  ccPromise = (async () => {
    let cc = null;
    try {
      const t = await (await fetch("https://www.cloudflare.com/cdn-cgi/trace")).text();
      const m = t.match(/loc=([A-Z]{2})/);
      if (m) cc = m[1];
    } catch (e) {}
    if (!cc) {
      try {
        const j = await (await fetch("https://api.country.is/")).json();
        if (j && /^[A-Z]{2}$/.test(j.country)) cc = j.country;
      } catch (e) {}
    }
    if (cc) { try { sessionStorage.setItem("ckl_click_cc", cc); } catch (e) {} }
    else ccPromise = null;
    return cc;
  })();
  return ccPromise;
}

// toolStats/clk_geo_d_YYYY-MM-DD = { total, countries: { BD: n, IN: n, Unknown: n } }
async function trackClickCountry(day) {
  try {
    const cc = (await getCountry()) || "Unknown";
    await setDoc(doc(db, "toolStats", "clk_geo_d_" + day), { total: increment(1), countries: { [cc]: increment(1) } }, { merge: true });
  } catch (e) {}
}

export async function trackUse(tool) {
 tool = tool || location.pathname.split("/").filter(Boolean).pop() || "unknown";
  const day = new Date().toISOString().slice(0, 10);
  try {
    await setDoc(doc(db, "toolStats", "totals"), { [tool]: increment(1), total: increment(1) }, { merge: true });
    await setDoc(doc(db, "toolStats", "d_" + day), { [tool]: increment(1), total: increment(1) }, { merge: true });
    await trackClickCountry(day);
  } catch (e) {}
}

export async function trackDownload(tool) {
  tool = tool || location.pathname.split("/").filter(Boolean).pop() || "unknown";
  const day = new Date().toISOString().slice(0, 10);
  try {
    await setDoc(doc(db, "toolStats", "dl_totals"), { [tool]: increment(1), total: increment(1) }, { merge: true });
    await setDoc(doc(db, "toolStats", "dl_d_" + day), { [tool]: increment(1), total: increment(1) }, { merge: true });
    await trackClickCountry(day);
  } catch (e) {}
}

if (!window.__dlHook) {
  window.__dlHook = true;
  let last = 0;
  const count = a => {
    if (!a || !a.hasAttribute || !a.hasAttribute("download")) return;
    if (!String(a.href).startsWith("blob:")) return;
    const now = Date.now();
    if (now - last < 800) return;
    last = now;
    trackDownload();
  };
  document.addEventListener("click", e => count(e.target.closest && e.target.closest("a")), true);
  const origClick = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () { count(this); return origClick.apply(this, arguments); };
  const origDispatch = HTMLAnchorElement.prototype.dispatchEvent;
  HTMLAnchorElement.prototype.dispatchEvent = function (ev) { if (ev && ev.type === "click") count(this); return origDispatch.apply(this, arguments); };
}
