document.getElementById('usuarioForm').onsubmit = async function (e) {
    e.preventDefault(); // Evitar el envío del formulario por defecto

    const usuario = document.getElementById('usuario').value;
    const clave = document.getElementById('clave').value;
    const nombre = document.getElementById('nombre').value;
    const direccion = document.getElementById('direccion').value;
    const telefono = document.getElementById('telefono').value;

    const response = await fetch('/usuarios', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ usuario, clave, nombre, direccion, telefono })
    });

    if (response.ok) {
        alert('Usuario registrado exitosamente');
        document.getElementById('usuarioForm').reset(); // Limpiar el formulario
    } else {
        const data = await response.json();
        alert(data.message); // Mostrar mensaje de error
    }
};
