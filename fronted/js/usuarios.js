document.getElementById("form-usuario").addEventListener("submit", function(event) {
  event.preventDefault();

  const data = {
    usuario: document.getElementById("usuario").value,
    clave: document.getElementById("clave").value,
    nombre: document.getElementById("nombre").value,
    direccion: document.getElementById("direccion").value,
    telefono: document.getElementById("telefono").value,
  };

  fetch("/registrar_usuario", {  // Utiliza rutas relativas
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert("Usuario registrado exitosamente.");
      cargarUsuarios();
      document.getElementById("form-usuario").reset();
    } else {
      alert("Error al registrar usuario.");
    }
  })
  .catch(error => {
    console.error("Error:", error);
  });
});

// Función para cargar y mostrar usuarios en la tabla
function cargarUsuarios() {
  fetch("/obtener_usuarios")
    .then(response => response.json())
    .then(data => {
      const tabla = document.getElementById("tabla-usuarios");
      tabla.innerHTML = "";

      data.forEach(usuario => {
        const fila = document.createElement("tr");

        fila.innerHTML = `
          <td>${usuario.idUsuario}</td>
          <td>${usuario.usuario}</td>
          <td>${usuario.nombre}</td>
          <td>${usuario.direccion}</td>
          <td>${usuario.telefono}</td>
          <td>
            <button class="editar" onclick="editarUsuario(${usuario.idUsuario})">Editar</button>
            <button class="eliminar" onclick="eliminarUsuario(${usuario.idUsuario})">Eliminar</button>
          </td>
        `;
        tabla.appendChild(fila);
      });
    })
    .catch(error => {
      console.error("Error:", error);
    });
}

// Función para buscar usuarios
function buscarUsuarios() {
  const nombre = document.getElementById("buscar").value;
  fetch(`/buscar_usuario?nombre=${encodeURIComponent(nombre)}`)
    .then(response => response.json())
    .then(data => {
      const tabla = document.getElementById("tabla-usuarios");
      tabla.innerHTML = "";

      data.forEach(usuario => {
        const fila = document.createElement("tr");

        fila.innerHTML = `
          <td>${usuario.idUsuario}</td>
          <td>${usuario.usuario}</td>
          <td>${usuario.nombre}</td>
          <td>${usuario.direccion}</td>
          <td>${usuario.telefono}</td>
          <td>
            <button class="editar" onclick="editarUsuario(${usuario.idUsuario})">Editar</button>
            <button class="eliminar" onclick="eliminarUsuario(${usuario.idUsuario})">Eliminar</button>
          </td>
        `;
        tabla.appendChild(fila);
      });
    })
    .catch(error => {
      console.error("Error:", error);
    });
}

// Función para obtener datos de un usuario específico
function obtenerUsuario(idUsuario) {
  return fetch(`/obtener_usuario/${idUsuario}`)
    .then(response => response.json())
    .then(data => data)
    .catch(error => {
      console.error("Error:", error);
      return null;
    });
}

// Función para editar un usuario
function editarUsuario(idUsuario) {
  obtenerUsuario(idUsuario).then(usuario => {
    if (usuario) {
      const nuevoUsuario = prompt("Nuevo nombre de usuario:", usuario.usuario) || usuario.usuario;
      const nuevaClave = prompt("Nueva clave:", usuario.clave) || usuario.clave;
      const nuevoNombre = prompt("Nuevo nombre:", usuario.nombre) || usuario.nombre;
      const nuevaDireccion = prompt("Nueva dirección:", usuario.direccion) || usuario.direccion;
      const nuevoTelefono = prompt("Nuevo teléfono:", usuario.telefono) || usuario.telefono;

      const data = {
        usuario: nuevoUsuario,
        clave: nuevaClave,
        nombre: nuevoNombre,
        direccion: nuevaDireccion,
        telefono: nuevoTelefono
      };

      fetch(`/actualizar_usuario/${idUsuario}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert("Usuario actualizado exitosamente.");
          cargarUsuarios();
        } else {
          alert("Error al actualizar usuario.");
        }
      })
      .catch(error => {
        console.error("Error:", error);
      });
    } else {
      alert("Usuario no encontrado.");
    }
  });
}

// Función para eliminar un usuario
function eliminarUsuario(idUsuario) {
  if (confirm("¿Estás seguro de eliminar este usuario?")) {
    fetch(`/eliminar_usuario/${idUsuario}`, {
      method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert("Usuario eliminado exitosamente.");
        cargarUsuarios();
      } else {
        alert("Error al eliminar usuario.");
      }
    })
    .catch(error => {
      console.error("Error:", error);
    });
}

// Cargar usuarios al iniciar la página
window.onload = cargarUsuarios;
