import { initializeApp, cert } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";
import nodemailer from "nodemailer";

// ---- settings you can tweak ----
const SITE = "https://convertkitlite.site";
const PAGES = ["/", "/tools/mergepdf/"];  // pages that must load
const ERR_MIN = 10;       // alert when today's errors reach this AND are 2x yesterday's
const DROP_MIN_AVG = 4;   // ignore traffic drops while normal traffic is below this per day
const DROP_RATIO = 0.4;   // alert when yesterday's visitors < 40% of the previous 7-day average
// --------------------------------

let sa;
try { sa = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT); }
catch { throw new Error("FIREBASE_SERVICE_ACCOUNT secret is missing or is not valid JSON"); }
const user = process.env.ALERT_GMAIL_USER, pass = process.env.ALERT_GMAIL_APP_PASSWORD;
if (!user || !pass) throw new Error("ALERT_GMAIL_USER / ALERT_GMAIL_APP_PASSWORD secrets are missing");

initializeApp({ credential: cert(sa) });
const db = getFirestore();
const transporter = nodemailer.createTransport({ service: "gmail", auth: { user, pass } });
const send = (subject, text) =>
  transporter.sendMail({ from: `ConvertKit Lite Alerts <${user}>`, to: user, subject, text });

const day = n => new Date(Date.now() - n * 864e5).toISOString().slice(0, 10);
const today = day(0), yesterday = day(1);
const get = async id => { const s = await db.collection("toolStats").doc(id).get(); return s.exists ? s.data() : {}; };
const ADMIN = SITE + "/admin/";

const topErrors = errs => Object.entries(errs || {}).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([k, v]) => {
  const i = k.indexOf("~");
  const page = (i < 0 ? "" : k.slice(0, i)).replace(/\|/g, "/") || "/";
  const msg = (i < 0 ? k : k.slice(i + 1)).replace(/_/g, " ");
  return `  ${v}x  ${msg}  (${page})`;
});

async function problem(path) {
  let why = "";
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const r = await fetch(SITE + path, { signal: AbortSignal.timeout(15000) });
      const t = await r.text();
      if (r.ok && /convertkit/i.test(t)) return "";
      why = `HTTP ${r.status}` + (r.ok ? " (page content looks wrong)" : "");
    } catch (e) { why = String(e.message || e); }
    if (attempt === 0) await new Promise(r => setTimeout(r, 10000));
  }
  return why;
}

const stateRef = db.collection("alertState").doc("state");
const state = (await stateRef.get()).data() || {};

// Test mode: workflow run with "Send a test email" ticked
if (process.env.TEST_EMAIL === "true") {
  const v = await get("geo_d_" + yesterday), e = await get("err_d_" + today);
  await send("[ConvertKit Lite] Test alert - email is working",
    `This is a test from your alert job.\n\nVisitors yesterday: ${v.total || 0}\nErrors today so far: ${e.total || 0}\n\nAdmin: ${ADMIN}`);
  console.log("Test email sent.");
  process.exit(0);
}

const alerts = [], next = {};

// 1) site down
const down = [];
for (const p of PAGES) { const why = await problem(p); if (why) down.push(`  ${SITE}${p}  ->  ${why}`); }
console.log("Site check:", down.length ? down : "all pages OK");
if (down.length && state.downDay !== today) {
  alerts.push({ title: "site problem", body: "These pages failed to load:\n" + down.join("\n") });
  next.downDay = today;
}

// 2) error spike
const eT = await get("err_d_" + today), eY = await get("err_d_" + yesterday);
const et = eT.total || 0, ey = eY.total || 0;
console.log(`Errors: today ${et}, yesterday ${ey}`);
if (et >= ERR_MIN && et >= 2 * ey && state.errDay !== today) {
  alerts.push({ title: "error spike", body: `${et} errors today so far (${ey} yesterday). Top errors:\n` + topErrors(eT.errs).join("\n") });
  next.errDay = today;
}

// 3) traffic drop (checked once per day)
if (state.dropDay !== today) {
  const y = (await get("geo_d_" + yesterday)).total || 0;
  let sum = 0;
  for (let i = 2; i <= 8; i++) sum += (await get("geo_d_" + day(i))).total || 0;
  const avg = sum / 7;
  console.log(`Visitors: yesterday ${y}, previous 7-day average ${avg.toFixed(1)}`);
  if (avg >= DROP_MIN_AVG && y <= avg * DROP_RATIO)
    alerts.push({ title: "traffic drop", body: `Yesterday had ${y} visitors; the previous 7-day average is ${avg.toFixed(1)} per day.` });
  next.dropDay = today;
}

if (alerts.length) {
  await send(`[ConvertKit Lite] ALERT: ${alerts.map(a => a.title).join(", ")}`,
    alerts.map(a => `== ${a.title.toUpperCase()} ==\n${a.body}`).join("\n\n") + `\n\nAdmin: ${ADMIN}`);
  console.log("Alert email sent:", alerts.map(a => a.title).join(", "));
} else console.log("No alerts.");

await stateRef.set({ ...next, updatedAt: new Date().toISOString() }, { merge: true });
