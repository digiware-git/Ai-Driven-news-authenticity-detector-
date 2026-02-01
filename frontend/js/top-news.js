const BACKEND_API = "http://127.0.0.1:8000";

// ===================================================
// ================= SAFE PAGE LOAD ==================
// ===================================================

document.addEventListener("DOMContentLoaded", () => {
  fetchTopNews();
});

// ===================================================
// ================= FETCH TOP NEWS ==================
// ===================================================

async function fetchTopNews() {
  try {
    const res = await fetch(`${BACKEND_API}/top-news`);
    if (!res.ok) throw new Error("Backend error");

    const data = await res.json();
    const container = document.getElementById("newsContainer");

    if (!container) return;

    container.innerHTML = "";

    if (!data.articles || data.articles.length === 0) {
      container.innerHTML = "<p>No news available</p>";
      return;
    }

    data.articles.forEach(article => {
      const fullText = [
        article.title,
        article.description || "",
        article.content || ""
      ].join(". ");

      const card = document.createElement("div");
      card.className = "card";

      const title = document.createElement("h3");
      title.innerText = article.title;

      const desc = document.createElement("p");
      desc.innerText = article.description || "No description available";

      const source = document.createElement("small");
      source.innerText = `Source: ${article.source?.name || "Unknown"}`;

      const btn = document.createElement("button");
      btn.innerText = "Verify with AI";

      // 🔥 FIX: NO inline onclick
      btn.addEventListener("click", () => {
        verifyNews(fullText);
      });

      card.appendChild(title);
      card.appendChild(desc);
      card.appendChild(source);
      card.appendChild(document.createElement("br"));
      card.appendChild(document.createElement("br"));
      card.appendChild(btn);

      container.appendChild(card);
    });

  } catch (err) {
    console.error("TOP NEWS ERROR:", err);
    alert("Failed to load news from backend");
  }
}

// ===================================================
// ================= VERIFY NEWS =====================
// ===================================================

async function verifyNews(text) {
  try {
    const res = await fetch(`${BACKEND_API}/verify-text`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    if (!res.ok) throw new Error("Verify failed");

    const data = await res.json();

    showModal(data);

    // 🔥 SAVE IN UNIFIED HISTORY
    if (window.addHistory) {
      addHistory("NEWS", data.label, data.confidence);
    }

  } catch (err) {
    console.error("VERIFY ERROR:", err);
    alert("Verification failed");
  }
}

// ===================================================
// ================= RESULT MODAL ====================
// ===================================================

function showModal(data) {
  const modal = document.getElementById("resultModal");
  if (!modal) return;

  modal.classList.remove("hidden");

  document.getElementById("modalLabel").innerText = data.label;
  document.getElementById("modalConfidence").innerText =
    `Confidence: ${data.confidence}%`;

  const bar = document.getElementById("modalBar");
  bar.style.width = data.confidence + "%";

  if (data.label === "FAKE") bar.style.background = "#ef4444";
  else if (data.label === "REAL") bar.style.background = "#22c55e";
  else bar.style.background = "#facc15";
}

function closeModal() {
  document.getElementById("resultModal")?.classList.add("hidden");
}
