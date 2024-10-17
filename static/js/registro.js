document.getElementById('formUsuario').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    
    fetch('/registrar_usuario', {
        method: 'POST',
        body: new URLSearchParams(formData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
