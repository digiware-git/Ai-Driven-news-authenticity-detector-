const API = "http://127.0.0.1:8000";

async function verifyText() {
  const text = document.getElementById("newsText").value.trim();
  if (!text) {
    alert("Please paste some news text");
    return;
  }

  const res = await fetch(`${API}/verify-text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  const data = await res.json();
  showResult(data);
}

function showResult(data) {
  document.getElementById("resultModal").classList.remove("hidden");

  const label = document.getElementById("resultLabel");
  const fill = document.getElementById("confidenceFill");

  label.innerText = data.label;
  document.getElementById("confidenceText").innerText =
    `Confidence: ${data.confidence}%`;

  fill.style.width = data.confidence + "%";

  if (data.label === "FAKE") fill.style.background = "#ef4444";
  else if (data.label === "REAL") fill.style.background = "#22c55e";
  else fill.style.background = "#facc15";

  const list = document.getElementById("explanationList");
  list.innerHTML = "";

  data.explanation.forEach(reason => {
    const li = document.createElement("li");
    li.innerText = reason;
    list.appendChild(li);
  });
}

function closeModal() {
  document.getElementById("resultModal").classList.add("hidden");
}
