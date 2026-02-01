// ================= URL VALIDATION =================
function isValidURL(url) {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

const API_BASE = "http://127.0.0.1:8000";

// ================= AUTO FROM TOP NEWS =================
const savedNews = localStorage.getItem("newsText");
if (savedNews && document.getElementById("textInput")) {
  document.getElementById("textInput").value = savedNews;
  localStorage.removeItem("newsText");
}

// ================= TEXT =================
async function verifyText() {
  const text = document.getElementById("textInput")?.value.trim();
  if (!text) return alert("Please enter some news text");

  const res = await fetch(`${API_BASE}/verify-text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  const data = await res.json();
  showResult(data);
  addHistory("TEXT", data.label, data.confidence);
}

// ================= URL =================
async function verifyURL() {
  const url = document.getElementById("urlInput")?.value.trim();

  if (!isValidURL(url)) {
    alert("Please enter a valid URL (https://...)");
    return;
  }

  const res = await fetch(`${API_BASE}/verify-url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  });

  const data = await res.json();
  showResult(data);
  addHistory("URL", data.label, data.confidence);
}

// ================= IMAGE =================
async function verifyImage() {
  const input = document.getElementById("imageInput");
  if (!input || !input.files.length) {
    alert("Please select an image");
    return;
  }

  const formData = new FormData();
  formData.append("file", input.files[0]);

  const res = await fetch(`${API_BASE}/verify-image`, {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  showResult(data);
  addHistory("IMAGE", data.label, data.confidence);
}

// ================= RESULT (BOX + MODAL) =================
function showResult(data) {

  // TEXT PAGE
  const box = document.getElementById("resultBox");
  if (box) box.classList.remove("hidden");

  // URL / IMAGE MODAL
  const modal = document.getElementById("resultModal");
  if (modal) modal.classList.remove("hidden");

  const label = document.getElementById("resultLabel");
  const fill = document.getElementById("confidenceFill");
  const text = document.getElementById("confidenceText");
  const list = document.getElementById("explanationList");

  if (!label || !fill || !text || !list) return;

  label.innerText = data.label;
  text.innerText = `Confidence: ${data.confidence}%`;
  fill.style.width = data.confidence + "%";

  fill.style.background =
    data.label === "REAL" ? "#22c55e" :
    data.label === "FAKE" ? "#ef4444" : "#facc15";

  list.innerHTML = "";
  (data.explanation || []).forEach(r => {
    const li = document.createElement("li");
    li.innerText = r;
    list.appendChild(li);
  });
}

function closeModal() {
  document.getElementById("resultModal")?.classList.add("hidden");
}

// ================= HISTORY =================
function addHistory(type, label, confidence) {
  const history = JSON.parse(localStorage.getItem("history")) || [];

  history.unshift({
    type,
    label,
    confidence,
    time: new Date().toLocaleString()
  });

  localStorage.setItem("history", JSON.stringify(history));

  const list = document.getElementById("historyList");
  if (list) {
    const li = document.createElement("li");
    li.innerText = `[${type}] ${label} (${confidence}%)`;
    list.prepend(li);
  }
}

// ================= URL PAGE BUTTON BIND =================
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("verifyUrlBtn");
  if (btn) btn.addEventListener("click", verifyURL);
});
