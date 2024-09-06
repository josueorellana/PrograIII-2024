from urllib import parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Hola Mundo".encode())

server = HTTPServer(('localhost', 3000), servidorBasico)
server.serve_forever()
print("Servidor ejecutado en el puerto 3000")