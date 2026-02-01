// ================= CONFIG =================
const API = "http://127.0.0.1:8000";

// ================= AUTH CHECK =================
function checkAuth(optional = false) {
  if (!localStorage.getItem("token") && !optional) {
    window.location.href = "login.html";
  }
}

console.log("AUTH.JS LOADED");

// ================= MODE =================
let mode = "login"; // login | signup

// ================= MODE SWITCH =================
function toggleMode() {
  mode = mode === "login" ? "signup" : "login";

  const emailField = document.getElementById("email");
  if (emailField) emailField.classList.toggle("hidden");

  const title = document.getElementById("formTitle");
  if (title) {
    title.innerText =
      mode === "login"
        ? "Sign In to continue"
        : "Create a new account";
  }

  const switchText = document.getElementById("switchText");
  if (switchText) {
    switchText.innerHTML =
      mode === "login"
        ? `Don't have an account?
           <span onclick="toggleMode()" style="color:#38bdf8; cursor:pointer;">
             Sign Up
           </span>`
        : `Already have an account?
           <span onclick="toggleMode()" style="color:#38bdf8; cursor:pointer;">
             Sign In
           </span>`;
  }
}

// ================= PASSWORD TOGGLE =================
function togglePassword() {
  const pwd = document.getElementById("password");
  if (!pwd) return;
  pwd.type = pwd.type === "password" ? "text" : "password";
}

// ================= SUBMIT AUTH =================
async function submitAuth() {
  const username = document.getElementById("username")?.value.trim();
  const password = document.getElementById("password")?.value.trim();
  const email = document.getElementById("email")?.value.trim();

  if (!username || !password) {
    alert("Username & password required");
    return;
  }

  let url = `${API}/login`;
  let payload = { username, password };

  if (mode === "signup") {
    if (!email) {
      alert("Email required");
      return;
    }
    url = `${API}/register`;
    payload = { username, email, password };
  }

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || "Authentication failed");
      return;
    }

    // ================= LOGIN SUCCESS =================
    if (mode === "login") {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("username", username);
      window.location.href = "index.html";
    } 
    // ================= SIGNUP SUCCESS =================
    else {
      alert("Registration successful. Please login.");
      toggleMode();
    }

  } catch (err) {
    alert("Server not reachable");
    console.error(err);
  }
}
