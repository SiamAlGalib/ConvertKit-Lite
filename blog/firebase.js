// Paste your Firebase web config here ONCE. Blog + admin both use this file.
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";
import { getDatabase } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-database.js";

const firebaseConfig = {
  apiKey: "AIzaSyBDDL4zLulL93bs9T710bXIeKCN3qHys4M",
  authDomain: "onvertkitlite.firebaseapp.com",
  databaseURL: "PASTE_YOUR_DATABASE_URL_HERE",
  projectId: "onvertkitlite",
  storageBucket: "onvertkitlite.firebasestorage.app",
  messagingSenderId: "469104121288",
  appId: "1:469104121288:web:fb31e363777fab7ba75cfd"
};

export const ADMIN_EMAILS = ["anowar531237@gmail.com"];
export const COL = "convertkitBlogPosts"; // Firestore collection name

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
export const rtdb = getDatabase(app);e(app);
