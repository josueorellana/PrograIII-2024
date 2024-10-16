document.getElementById('loginForm').onsubmit = async function (e) {
    e.preventDefault(); // Evitar el envío del formulario por defecto

    const usuario = document.getElementById('usuario').value;
    const clave = document.getElementById('clave').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ usuario, clave })
    });

    if (response.ok) {
        // Redirigir a la ruta de usuarios después de un inicio de sesión exitoso
        window.location.href = '/usuarios';
    } else {
        const data = await response.json();
        alert(data.message); // Mostrar mensaje de error
    }
};
