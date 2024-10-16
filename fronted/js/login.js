// frontend/js/login.js

document.getElementById("form-login").addEventListener("submit", function(event) {
  event.preventDefault();

  const data = {
    usuario: document.getElementById("usuario").value,
    clave: document.getElementById("clave").value
  };

  fetch("/login", {  // Utiliza rutas relativas
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      window.location.href = "/usuarios"; // Redirige a la página de usuarios
    } else {
      alert("Acceso denegado. Usuario o clave incorrectos.");
    }
  })
  .catch(error => {
    console.error("Error:", error);
  });
});
