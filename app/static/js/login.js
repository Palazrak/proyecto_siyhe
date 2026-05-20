const form = document.getElementById("loginForm");
const feedback = document.getElementById("feedback");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const usuario = document.getElementById("usuario").value.trim();
  const password = document.getElementById("password").value.trim();

  feedback.textContent = "";
  feedback.className = "feedback";

  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario, password }),
    });

    const raw = await response.text();
    let data = {};
    try {
      data = raw ? JSON.parse(raw) : {};
    } catch (_err) {
      data = { detail: raw || "Error interno del servidor" };
    }

    if (!response.ok) {
      throw new Error(data.detail || "No se pudo iniciar sesión");
    }

    localStorage.setItem("usuario_actual", data.usuario);
    window.location.href = "/placas";
  } catch (error) {
    feedback.textContent = error.message;
    feedback.classList.add("error");
  }
});
