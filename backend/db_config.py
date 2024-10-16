import mysql.connector
from mysql.connector import Error

def create_database_and_table():
    try:
        # Conectar a MySQL
        connection = mysql.connector.connect(
            host='localhost',  # Cambia esto si tu servidor MySQL está en otra dirección
            user='',  # Reemplaza con tu usuario de MySQL
            password=''  # Reemplaza con tu contraseña de MySQL
        )

        if connection.is_connected():
            cursor = connection.cursor()
            # Crear la base de datos
            cursor.execute("CREATE DATABASE IF NOT EXISTS db_academica")
            print("Base de datos 'db_academica' creada con éxito.")

            # Seleccionar la base de datos
            cursor.execute("USE db_academica")

            # Crear la tabla usuarios
            create_table_query = """
            CREATE TABLE IF NOT EXISTS usuarios (
                idUsuario INT(10) AUTO_INCREMENT PRIMARY KEY,
                usuario CHAR(35) NOT NULL,
                clave CHAR(35) NOT NULL,
                nombre CHAR(85),
                direccion CHAR(100),
                telefono CHAR(9)
            )
            """
            cursor.execute(create_table_query)
            print("Tabla 'usuarios' creada con éxito.")

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada.")

if __name__ == "__main__":
    create_database_and_table()

