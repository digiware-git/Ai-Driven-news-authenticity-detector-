const API_BASE = "http://127.0.0.1:8000";

function previewImage() {
  const input = document.getElementById("imageInput");
  const previewBox = document.getElementById("previewBox");
  const img = document.getElementById("imagePreview");

  if (!input.files || !input.files[0]) return;

  const reader = new FileReader();
  reader.onload = () => {
    img.src = reader.result;
    previewBox.classList.remove("hidden");
  };

  reader.readAsDataURL(input.files[0]);
}

async function verifyImage() {
  const input = document.getElementById("imageInput");

  if (!input.files || input.files.length === 0) {
    alert("Please select an image");
    return;
  }

  const formData = new FormData();
  formData.append("file", input.files[0]);

  try {
    const res = await fetch(`${API_BASE}/verify-image`, {
      method: "POST",
      body: formData
    });

    if (!res.ok) throw new Error("Backend error");

    const data = await res.json();

    showResult(data);
    addHistory("IMAGE", data.label, data.confidence);

  } catch (err) {
    console.error(err);
    alert("Image verification failed");
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
