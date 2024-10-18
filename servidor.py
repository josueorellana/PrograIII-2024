from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import json
import urllib.parse

def conexion_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_academica"
    )

class ManejadorServidor(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.path = "/login.html"
        elif self.path == "/listar_usuarios":
            self.listar_usuarios()
            return
        elif self.path.startswith("/editar_usuario"):
            self.editar_usuario_form()
            return
        
        try:
            if self.path.endswith(".html") or self.path.endswith(".js"):
                file_to_open = open("templates" + self.path).read() if self.path.endswith(".html") else open("static/js" + self.path).read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(bytes(file_to_open, "utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            print(f"Error al servir el archivo: {e}")
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/registrar_usuario":
            self.registrar_usuario()
        elif self.path == "/login":
            self.login()
        elif self.path == "/actualizar_usuario":
            self.actualizar_usuario()

    def do_DELETE(self):
        if self.path.startswith("/eliminar_usuario"):
            self.eliminar_usuario()

    def listar_usuarios(self):
        conexion = conexion_bd()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(usuarios).encode('utf-8'))


    def eliminar_usuario(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        id_usuario = params.get('id', [None])[0]

        if id_usuario:
            conexion = conexion_bd()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM usuarios WHERE IdUsuario = %s", (id_usuario,))
            conexion.commit()
            cursor.close()
            conexion.close()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": "Usuario eliminado correctamente"}).encode('utf-8'))
        else:
            self.send_response(400)
            self.end_headers()

    def editar_usuario_form(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        id_usuario = params.get('id', [None])[0]

        if id_usuario:
            conexion = conexion_bd()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE IdUsuario = %s", (id_usuario,))
            usuario = cursor.fetchone()
            cursor.close()
            conexion.close()

            if usuario:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                
                html_response = f"""
                <!DOCTYPE html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Editar Usuario</title>
                </head>
                <body>
                    <h1>Editar Usuario</h1>
                    <form id="form_editar_usuario">
                        <input type="hidden" name="id" value="{usuario['IdUsuario']}">
                        <label for="usuario">Usuario:</label>
                        <input type="text" name="usuario" value="{usuario['usuario']}"><br>
                        <label for="clave">Clave:</label>
                        <input type="text" name="clave" value="{usuario['clave']}"><br>
                        <label for="nombre">Nombre:</label>
                        <input type="text" name="nombre" value="{usuario['nombre']}"><br>
                        <label for="direccion">Dirección:</label>
                        <input type="text" name="direccion" value="{usuario['direccion']}"><br>
                        <label for="telefono">Teléfono:</label>
                        <input type="text" name="telefono" value="{usuario['telefono']}"><br>
                        <button type="submit">Guardar Cambios</button>
                    </form>
                    <script>
                        document.getElementById('form_editar_usuario').addEventListener('submit', function(e) {{
                            e.preventDefault();
                            const formData = new FormData(this);
                            fetch('/actualizar_usuario', {{
                                method: 'POST',
                                body: formData
                            }}).then(response => response.json())
                            .then(data => {{
                                alert(data.message);
                                if (data.success) {{
                                    window.location.href = '/listar_usuarios.html';
                                }}
                            }}).catch(error => console.error('Error:', error));
                        }});
                    </script>
                </body>
                </html>
                """
                self.wfile.write(html_response.encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()

    def registrar_usuario(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        datos = urllib.parse.parse_qs(post_data)

        conexion = conexion_bd()
        cursor = conexion.cursor()
        sql = "INSERT INTO usuarios (usuario, clave, nombre, direccion, telefono) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (datos['usuario'][0], datos['clave'][0], datos['nombre'][0], datos['direccion'][0], datos['telefono'][0]))
        conexion.commit()
        cursor.close()
        conexion.close()

        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "message": "Usuario registrado correctamente"}).encode('utf-8'))

    def login(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        datos = urllib.parse.parse_qs(post_data)

        conexion = conexion_bd()
        cursor = conexion.cursor()

        sql = "SELECT * FROM usuarios WHERE usuario=%s AND clave=%s"
        cursor.execute(sql, (datos['usuario'][0], datos['clave'][0]))
        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
        else:
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False}).encode('utf-8'))

    def actualizar_usuario(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        datos = urllib.parse.parse_qs(post_data)

        if 'id' in datos:
            conexion = conexion_bd()
            cursor = conexion.cursor()
            sql = """
            UPDATE usuarios SET usuario=%s, clave=%s, nombre=%s, direccion=%s, telefono=%s WHERE IdUsuario=%s
            """
            cursor.execute(sql, (datos['usuario'][0], datos['clave'][0], datos['nombre'][0], datos['direccion'][0], datos['telefono'][0], datos['id'][0]))
            conexion.commit()
            cursor.close()
            conexion.close()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": "Usuario actualizado correctamente"}).encode('utf-8'))
        else:
            self.send_response(400)
            self.end_headers()

def run():
    puerto = 5000
    servidor = HTTPServer(('localhost', puerto), ManejadorServidor)
    print(f"Servidor corriendo en http://localhost:{puerto}")
    servidor.serve_forever()

if __name__ == "__main__":
    run()
