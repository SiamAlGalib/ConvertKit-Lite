cat > stats.js <<'EOF'
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

export async function trackUse(tool) {
 tool = tool || location.pathname.split("/").filter(Boolean).pop() || "unknown";
  const day = new Date().toISOString().slice(0, 10);
  try {
    await setDoc(doc(db, "toolStats", "totals"), { [tool]: increment(1), total: increment(1) }, { merge: true });
    await setDoc(doc(db, "toolStats", "d_" + day), { [tool]: increment(1), total: increment(1) }, { merge: true });
  } catch (e) {}
}
EOF