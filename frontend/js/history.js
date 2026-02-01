// ===================================================
// ================= HISTORY STORAGE =================
// ===================================================

window.addHistory = function (type, label, confidence) {
  const history = JSON.parse(localStorage.getItem("history")) || [];

  history.unshift({
    type,              // TEXT / URL / IMAGE
    label,             // REAL / FAKE / UNCERTAIN
    confidence,
    time: new Date().toLocaleString()
  });

  localStorage.setItem("history", JSON.stringify(history));

  // Live update (agar page par historyList hai)
  renderHistory();
};

// ===================================================
// ================= HISTORY RENDER ==================
// ===================================================

function renderHistory() {
  const list = document.getElementById("historyList");
  if (!list) return; // 🔥 SAFE EXIT

  const history = JSON.parse(localStorage.getItem("history")) || [];
  list.innerHTML = "";

  if (history.length === 0) {
    const li = document.createElement("li");
    li.innerText = "No verification history yet";
    li.style.opacity = "0.6";
    list.appendChild(li);
    return;
  }

  history.forEach(item => {
    const li = document.createElement("li");
    li.innerText = `[${item.time}] ${item.type} → ${item.label} (${item.confidence}%)`;
    list.appendChild(li);
  });
}

// ===================================================
// ================= SAFE AUTO LOAD ==================
// ===================================================

document.addEventListener("DOMContentLoaded", () => {
  renderHistory();
});
