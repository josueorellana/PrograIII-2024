import crud_academico
db = crud_academico.crud()

class crud_alumno:
    def consultar(self, buscar):
        return db.consultar("SELECT * FROM alumnos WHERE nombre like '%" + buscar["buscar"] + "%'")
    
    def administrar(self, datos):
        sql = """
            INSERT INTO alumnos (codigo, nombre, direccion, telefono, email)
            VALUES (%s, %s, %s, %s, %s) 
        """
        valores = (datos["codigo"], datos["nombre"], datos["direccion"], datos["telefono"], datos["correo"])
        return db.procesar_consultas(sql, valores)