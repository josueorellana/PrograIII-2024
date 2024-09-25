from urllib import parse
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import crud_alumno

crudAlumno = crud_alumno.crud_alumno()
class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
        url_parseada = urlparse(self.path)
        path = url_parseada.path
        parametros = parse_qs(url_parseada.query)

        if path == '/':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif path == '/vista':
            self.path = '/modulos/' + parametros['form'][0] + '.html'
            return SimpleHTTPRequestHandler.do_GET(self)

        elif path == '/alumnos':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(crudAlumno.consultar()).encode('utf-8'))
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