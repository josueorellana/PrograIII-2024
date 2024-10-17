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
        try:
            if self.path.endswith(".html") or self.path.endswith(".js"):
                file_to_open = open("templates" + self.path).read() if self.path.endswith(".html") else open("static/js" + self.path).read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")  # Especificar el tipo de contenido
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
        if self.path == "/login":
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


def run():
    puerto = 5000
    servidor = HTTPServer(('localhost', puerto), ManejadorServidor)
    print(f"Servidor corriendo en http://localhost:{puerto}")
    servidor.serve_forever()

if __name__ == "__main__":
    run()
