document.addEventListener("DOMContentLoaded", async function () {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please login again.");
    window.location.href = "/login";
    return;
  }

  try {
    const response = await fetch("/api/profile", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token }),
    });

    const data = await response.json();

    if (response.ok) {
      document.getElementById("username").value = data.username || "";
      document.getElementById("email").value = data.email || "";
      document.getElementById("age").value = data.age || "";
      document.getElementById("dob").value = data.dob || "";
      document.getElementById("contact").value = data.contact || "";
    } else {
      alert(data.error || "Failed to fetch profile.");
    }
  } catch (err) {
    console.error("Profile fetch failed:", err);
    alert("Network error while fetching profile.");
  }
});