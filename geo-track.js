/**
 * ConvertKit Lite - visitor geo tracker
 * Counts ONE visitor per browser per UTC day, grouped by country + continent.
 * Stores only counters (no IP address, no personal data) in Firestore:
 *   toolStats/geo_d_YYYY-MM-DD = { total, continents:{Asia:n,...}, countries:{BD:n,...} }
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

(async function track() {
  try {
    if (location.pathname.startsWith("/admin")) return; // never count yourself in the admin panel
    const day = new Date().toISOString().slice(0, 10);
    if (localStorage.getItem("ckl_geo_day") === day) return; // already counted today
    const cc = await getCountry();
    if (!cc) return;
    const continent = MAP[cc] || "Unknown";
    await setDoc(
      doc(db, "toolStats", "geo_d_" + day),
      { total: increment(1), continents: { [continent]: increment(1) }, countries: { [cc]: increment(1) } },
      { merge: true }
    );
    localStorage.setItem("ckl_geo_day", day);
  } catch (e) {
    console.warn("geo-track skipped:", e && e.message);
  }
})();
