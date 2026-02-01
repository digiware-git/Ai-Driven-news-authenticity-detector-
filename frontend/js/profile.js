document.addEventListener("DOMContentLoaded", () => {
  const profileBox = document.getElementById("profileBox");
  if (!profileBox) return;

  // ================= TOGGLE DROPDOWN =================
  profileBox.addEventListener("click", (e) => {
    e.stopPropagation(); // 🔥 outside click issue fix
    profileBox.classList.toggle("active");
  });

  // ================= CLOSE ON OUTSIDE CLICK =================
  document.addEventListener("click", () => {
    profileBox.classList.remove("active");
  });

  // ================= LOAD USER =================
  const username = localStorage.getItem("username");
  if (username) {
    const label = document.getElementById("usernameLabel");
    const avatar = document.getElementById("avatarText");

    if (label) label.innerText = username;
    if (avatar) avatar.innerText = username.charAt(0).toUpperCase();
  }
});

// ================= LOGOUT =================
function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  window.location.href = "login.html";
}
