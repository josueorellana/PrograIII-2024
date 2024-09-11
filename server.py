from urllib import parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import crud_alumno

crudAlumno = crud_alumno.crud_alumno()
class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)
    def do_POST(self):
        longitud = int(self.headers['Content-Length'])
        body = self.rfile.read(longitud)
        datos = body.decode('utf-8')
        datos = parse.unquote(datos)
        datos = json.loads(datos)
        resp = {"msg": crudAlumno.administrar(datos)}

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode('utf-8'))

server = HTTPServer(('localhost', 3000), servidorBasico)
print("Servidor ejecutado en el puerto 3000")
server.serve_forever()