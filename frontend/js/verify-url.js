const API_BASE = "http://127.0.0.1:8000";

function isValidURL(url) {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

async function verifyURL() {
  const url = document.getElementById("urlInput").value.trim();

  if (!isValidURL(url)) {
    alert("Please enter a valid URL (https://...)");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/verify-url`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });

    if (!res.ok) throw new Error("Backend error");

    const data = await res.json();

    showResult(data);
    addHistory("URL", data.label, data.confidence);

  } catch (err) {
    console.error(err);
    alert("URL verification failed");
  }
}

function showResult(data) {
  document.getElementById("resultModal").classList.remove("hidden");

  document.getElementById("resultLabel").innerText = data.label;
  document.getElementById("confidenceText").innerText =
    `Confidence: ${data.confidence}%`;

  const fill = document.getElementById("confidenceFill");
  fill.style.width = data.confidence + "%";

  if (data.label === "FAKE") fill.style.background = "#ef4444";
  else if (data.label === "REAL") fill.style.background = "#22c55e";
  else fill.style.background = "#facc15";

  const list = document.getElementById("explanationList");
  list.innerHTML = "";

  (data.explanation || []).forEach(reason => {
    const li = document.createElement("li");
    li.innerText = reason;
    list.appendChild(li);
  });
}

function closeModal() {
  document.getElementById("resultModal").classList.add("hidden");
}
