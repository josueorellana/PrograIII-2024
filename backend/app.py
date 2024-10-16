# backend/app.py

from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Permite solicitudes desde el frontend

# Conexión a la base de datos MySQL
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Reemplaza con tu usuario de MySQL
        password="",   # Reemplaza con tu contraseña de MySQL
        database="db_academica"
    )

# Ruta para servir la página de login
@app.route('/')
def serve_login():
    return send_from_directory(app.static_folder, 'login.html')

# Ruta para servir la página de gestión de usuarios
@app.route('/usuarios')
def serve_usuarios():
    return send_from_directory(app.static_folder, 'usuarios.html')

# API Endpoint para registrar un nuevo usuario
@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    data = request.json
    conn = conectar_db()
    cursor = conn.cursor()

    try:
        sql = "INSERT INTO usuarios (usuario, clave, nombre, direccion, telefono) VALUES (%s, %s, %s, %s, %s)"
        valores = (data['usuario'], data['clave'], data['nombre'], data['direccion'], data['telefono'])
        cursor.execute(sql, valores)
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False})
    finally:
        cursor.close()
        conn.close()

# API Endpoint para obtener todos los usuarios
@app.route('/obtener_usuarios', methods=['GET'])
def obtener_usuarios():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(usuarios)

# API Endpoint para buscar usuarios por nombre o usuario
@app.route('/buscar_usuario', methods=['GET'])
def buscar_usuario():
    nombre = request.args.get('nombre', default='', type=str)
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM usuarios WHERE nombre LIKE %s OR usuario LIKE %s", ("%" + nombre + "%", "%" + nombre + "%"))
    usuarios = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(usuarios)

# API Endpoint para obtener un usuario específico
@app.route('/obtener_usuario/<int:idUsuario>', methods=['GET'])
def obtener_usuario(idUsuario):
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM usuarios WHERE idUsuario = %s", (idUsuario,))
        usuario = cursor.fetchone()
        
        if usuario:
            return jsonify(usuario)
        else:
            return jsonify(None)
    except Exception as e:
        print(e)
        return jsonify(None)
    finally:
        cursor.close()
        conn.close()

# API Endpoint para actualizar un usuario
@app.route('/actualizar_usuario/<int:idUsuario>', methods=['PUT'])
def actualizar_usuario(idUsuario):
    data = request.json
    conn = conectar_db()
    cursor = conn.cursor()
    
    sql = "UPDATE usuarios SET usuario = %s, clave = %s, nombre = %s, direccion = %s, telefono = %s WHERE idUsuario = %s"
    valores = (data['usuario'], data['clave'], data['nombre'], data['direccion'], data['telefono'], idUsuario)
    
    try:
        cursor.execute(sql, valores)
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False})
    finally:
        cursor.close()
        conn.close()

# API Endpoint para eliminar un usuario
@app.route('/eliminar_usuario/<int:idUsuario>', methods=['DELETE'])
def eliminar_usuario(idUsuario):
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM usuarios WHERE idUsuario = %s", (idUsuario,))
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False})
    finally:
        cursor.close()
        conn.close()

# API Endpoint para login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND clave = %s", (data['usuario'], data['clave']))
        usuario = cursor.fetchone()
        
        if usuario:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})
    except Exception as e:
        print(e)
        return jsonify({"success": False})
    finally:
        cursor.close()
        conn.close()

# Ruta para manejar rutas inexistentes
@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'login.html')  # Redirige a login.html o muestra una página de error personalizada

if __name__ == '__main__':
    app.run(debug=True)
