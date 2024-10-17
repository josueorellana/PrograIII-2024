document.getElementById('formLogin').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    fetch('/login', {
        method: 'POST',
        body: new URLSearchParams(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {

            window.location.href = "/registro_usuario.html";
        } else {
            alert('Usuario o clave incorrecta');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
