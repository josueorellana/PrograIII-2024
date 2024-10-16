import http.server
import socketserver
import mysql.connector
import json
import os

PORT = 8000
DB_FILE = 'usuarios.db'

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('static/login.html', 'r') as file:
                self.wfile.write(file.read().encode())
        elif self.path == '/usuarios':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('static/usuarios.html', 'r') as file:
                self.wfile.write(file.read().encode())
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == '/usuarios':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            # Extraer datos
            usuario = data['usuario']
            clave = data['clave']
            nombre = data['nombre']
            direccion = data['direccion']
            telefono = data['telefono']

            try:
                # Conectar a la base de datos
                connection = mysql.connector.connect(
                    host='localhost',
                    user='root',  # Cambia esto con tu usuario
                    password='',  # Cambia esto con tu contraseña
                    database='db_academica'
                )
                cursor = connection.cursor()
                # Insertar usuario
                cursor.execute("INSERT INTO usuarios (usuario, clave, nombre, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
                               (usuario, clave, nombre, direccion, telefono))
                connection.commit()
                cursor.close()
                connection.close()

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Usuario registrado exitosamente'}).encode())
            except mysql.connector.Error as err:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message': f'Error: {err}'}).encode())
        else:
            self.send_error(404, "Not Found")

# Iniciar el servidor
with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Servidor corriendo en http://localhost:{PORT}")
    httpd.serve_forever()
