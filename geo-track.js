/**
 * ConvertKit Lite - visitor geo tracker
 * Counts ONE real visitor per browser per UTC day, grouped by country + continent.
 * Stores only counters (no IP address, no personal data) in Firestore:
 *   toolStats/geo_d_YYYY-MM-DD = { total, continents:{Asia:n,...}, countries:{BD:n,...} }
 *
 * A visit is counted only if:
 *   - it is not the admin panel
 *   - it is not an obvious bot / automated browser
 *   - the visitor interacts with the page (scroll, click, key, touch, mouse move)
 *     and stays at least 3 seconds
 *   - the tab is visible when the count is sent
 *
 * Add to every public page (before </body>):
 *   <script type="module" src="/geo-track.js"></script>
 */
import { db } from "/blog/firebase.js";
import { doc, setDoc, increment } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const GROUPS = {
  Asia: "AF AM AZ BH BD BT BN KH CN CY GE HK IN ID IR IQ IL JP JO KZ KW KG LA LB MO MY MV MN MM NP KP OM PK PS PH QA SA SG KR LK SY TW TJ TH TL TR TM AE UZ VN YE",
  Europe: "AL AD AT BY BE BA BG HR CZ DK EE FO FI FR DE GI GR GG VA HU IS IE IM IT JE XK LV LI LT LU MT MD MC ME NL MK NO PL PT RO RU SM RS SK SI ES SJ SE CH UA GB AX",
  Africa: "DZ AO BJ BW BF BI CM CV CF TD KM CG CD CI DJ EG GQ ER SZ ET GA GM GH GN GW KE LS LR LY MG MW ML MR MU YT MA MZ NA NE NG RE RW SH ST SN SC SL SO ZA SS SD TZ TG TN UG EH ZM ZW",
  NorthAmerica: "AI AG AW BS BB BZ BM BQ VG CA KY CR CU CW DM DO SV GL GD GP GT HT HN JM MQ MX MS NI PA PR BL KN LC MF PM VC SX TT TC US VI UM",
  SouthAmerica: "AR BO BR CL CO EC FK GF GY PY PE SR UY VE",
  Oceania: "AU NZ FJ PG SB VU NC PF WS TO KI FM MH PW NR TV CK NU TK WF GU MP AS PN NF CC CX HM",
  Antarctica: "AQ BV GS TF"
};
const MAP = {};
for (const [continent, list] of Object.entries(GROUPS)) list.split(" ").forEach(c => (MAP[c] = continent));

const BOT_RE = /bot|crawl|spider|slurp|headless|lighthouse|pagespeed|monitor|preview|python|curl|wget|axios|phantom|selenium|puppeteer|playwright/i;

async function getCountry() {
  try {
    const t = await (await fetch("https://www.cloudflare.com/cdn-cgi/trace")).text();
    const m = t.match(/loc=([A-Z]{2})/);
    if (m) return m[1];
  } catch (e) {}
  try {
    const j = await (await fetch("https://api.country.is/")).json();
    if (j && /^[A-Z]{2}$/.test(j.country)) return j.country;
  } catch (e) {}
  return null;
}

// Resolves only after a real interaction AND at least 3 seconds on the page
function waitForHuman() {
  return new Promise(resolve => {
    const start = Date.now();
    const events = ["pointerdown", "keydown", "scroll", "touchstart", "mousemove"];
    const fire = () => {
      events.forEach(e => removeEventListener(e, fire));
      setTimeout(resolve, Math.max(0, 3000 - (Date.now() - start)));
    };
    events.forEach(e => addEventListener(e, fire, { passive: true, once: true }));
  });
}

(async function track() {
  const day = new Date().toISOString().slice(0, 10);
  try {
    if (location.pathname.startsWith("/admin")) return; // never count yourself in the admin panel
    if (navigator.webdriver || BOT_RE.test(navigator.userAgent)) return; // skip bots
    if (localStorage.getItem("ckl_geo_day") === day) return; // already counted today

    // Mark as counted BEFORE any async work, so parallel tabs/pages can't double count
    localStorage.setItem("ckl_geo_day", day);

    await waitForHuman();
    if (document.visibilityState !== "visible") throw new Error("hidden");

    const cc = await getCountry();
    if (!cc) throw new Error("no country");
    const continent = MAP[cc] || "Unknown";
    await setDoc(
      doc(db, "toolStats", "geo_d_" + day),
      { total: increment(1), continents: { [continent]: increment(1) }, countries: { [cc]: increment(1) } },
      { merge: true }
    );
  } catch (e) {
    localStorage.removeItem("ckl_geo_day"); // failed, so allow a retry on the next load
    console.warn("geo-track skipped:", e && e.message);
  }
})();