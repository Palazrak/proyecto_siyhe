const form = document.getElementById("placaForm");
const feedback = document.getElementById("feedback");
const modal = document.getElementById("phishingModal");
const closeModalButton = document.getElementById("closeModal");

const usuario = localStorage.getItem("usuario_actual");
if (!usuario) {
  window.location.href = "/";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const placa = document.getElementById("placa").value.trim();
  feedback.textContent = "";
  feedback.className = "feedback";

  if (!placa) {
    feedback.textContent = "Ingresa una placa para continuar.";
    feedback.classList.add("error");
    return;
  }

  try {
    const response = await fetch("/api/placa", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario, placa }),
    });

    const raw = await response.text();
    let data = {};
    try {
      data = raw ? JSON.parse(raw) : {};
    } catch (_err) {
      data = { detail: raw || "Error interno del servidor" };
    }

    if (!response.ok) {
      throw new Error(data.detail || "No se pudo guardar la placa");
    }

    feedback.textContent = "Placa capturada correctamente.";
    feedback.classList.add("success");
    openModal();
  } catch (error) {
    feedback.textContent = error.message;
    feedback.classList.add("error");
  }
});

function openModal() {
  modal.classList.remove("d-none");
  modal.setAttribute("aria-hidden", "false");
  document.body.classList.add("modal-open");
}

function closeModal() {
  modal.classList.add("d-none");
  modal.setAttribute("aria-hidden", "true");
  document.body.classList.remove("modal-open");
}

closeModalButton.addEventListener("click", closeModal);

modal.addEventListener("click", (event) => {
  if (event.target === modal) {
    closeModal();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !modal.classList.contains("d-none")) {
    closeModal();
  }
});
