from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector, unicodedata

app = Flask(__name__)
app.secret_key = 'supersecretkey'

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'sivar_tours'
}
# Conexion con la base de datos
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Normalizacion del texto y manejo de palabras clave 
def normalizar(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()

# Autenticacion Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('username')
        password = request.form.get('password')
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and user['password'] == password: 
            return jsonify(success=True, message="Inicio de sesion exitoso", redirect="/menu")
        else:
            return jsonify(success=False, message="Credenciales incorrectas")
    return render_template('login.html')

# Autenticacion Registro de usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')

        if not correo or not password:
            flash('Todos los campos son obigatorios', 'error')
            return redirect(url_for('registro'))
        
        conn = get_db_connection()
        cursor = conn.cursor()

        #Validar correos existentes
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        if cursor.fetchone():
            flash('El correo ya esta registrado', 'error')
            conn.close()
            return redirect(url_for('registro'))
        
        # Insertar nuevos usuarios
        try:
            cursor.execute("INSERT INTO usuarios (correo, password) VALUES (%s, %s)", (correo, password))
            conn.commit()
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error al registrar usuario: {e}', 'error')
        finally:
            conn.close()

    return render_template('registro.html')

#Lugares turisticos de la aplicacion
lugares_turisticos = {
   "BINAES": ("Biblioteca Nacional de El Salvador fue fundada en 1870 y es un lugar emblemático que preserva y promueve "
               "la riqueza literaria, histórica y cultural del país. En sus instalaciones se realizan actividades como "
               "exposiciones, talleres, conferencias y eventos literarios."),
    "Finca Rauda": ("La Finca Rauda es un destino turístico rural ubicado en Chalchuapa, departamento de Santa Ana, "
                    "El Salvador. Es conocida por ofrecer una experiencia auténtica de contacto con la naturaleza, "
                    "cultura y tradición salvadoreña."),
    "El Malecon": ("El Malecón de la Libertad es uno de los destinos más populares para disfrutar de la costa y el" 
                   "mar en El Salvador, ubicado en el municipio de La Libertad, un lugar ideal para relajarse y disfrutar"  
                   "de la belleza del océano Pacífico."),
    "Mirador de Cristal": ("El mirador de cristal de Alegría, Usulután, es un atractivo turístico que consiste en una"  
                           "estructura de cristal que hace que los visitantes se sientan como si estuvieran en el aire" 
                           "Son cerca de 10 metros de piso de cristal que ofrecen una experiencia única. Algunos de los" 
                           "visitantes, en un primer momento, no se animan a caminar por el piso transparente. Sin embargo," 
                           "las ganas de vivir una nueva aventura les impulsan a perder el miedo. "),
    "Mirador": ("En El Salvadpr existen diversos citios que cuentan con miradores hacie una vista impresionante" 
                "Entre ellos estan, EL mirador de cristal en alegria ubicado en Finda Rauda y Mirador en puerta del diablo"
                "Necesitas mas informacion sobre alguno de estos?"),
    "Ruta de las Flores": ("La Ruta de las Flores es una de las experiencias turísticas más encantadoras de El Salvador," 
                        "ubicada en la región occidental del país. Es conocida por sus pintorescos pueblos coloniales, llenos de calles empedradas," 
                        "murales vibrantes y una rica combinación de cultura, gastronomía y naturaleza."),
    "Cerro el Pital": ("El Cerro El Pital, ubicado en el departamento de Chalatenango, es la montaña más alta" 
                    "de El Salvador, con una altitud de 2,730 metros sobre el nivel del mar. Este lugar es reconocido por su clima" 
                    "fresco y su vegetación diversa, que incluye bosques nubosos y una rica variedad de flora, como hortensias, cartuchos y girasoles. En cuanto a fauna, es hogar de especies como el quetzal, el tucán y el venado cola blanca, entre otros​"),
    "Que bueno": ("Claro puedo responder cualquier consulta que tengas"),
    "Genial": ("Si"),
    "Cuales son los mejores lugares para senderismo?": ("Aqui tienes algunos de los lugares para realizar actividades como senderismo en El Salvador" 
                                                        "Parque Nacional El Imposible" 
                                                        "Es uno de los mejores lugares con senderos diversos que llevan a cascadas y miradores espectaculares"
                                                        "Volcán de Santa Ana" 
                                                        "Ofrece una caminata volcánica con vistas al lago Coatepeque desde la cima."
                                                        "Parque Nacional El Boquerón" 
                                                        "Ubicado en el cráter del volcán San Salvador, ideal para caminatas" 
                                                        "cortas con vistas panorámicas."),
    "Perquin": ("Perquín, ubicado en el departamento de Morazán, es un destino turístico de gran relevancia histórica y natural en El Salvador, conocido como la Capital de la Ruta de la Paz"
                "Durante la Guerra Civil Salvadoreña, esta zona fue un epicentro"
                "de enfrentamientos, y actualmente conserva vestigios de este período como parte de su oferta turística."),
                                                       
    "Hola": "Hola, estoy aquí para asistirte. ¿En qué puedo ayudarte?",
}




usuarios = {
    "admin": "1234",
    "admin2": "2468"
}



@app.route('/')
def home():
    return render_template('bienvenida.html')

# Mostrar registros
@app.route('/transporte')
def transporte():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transporte")
    registros = cursor.fetchall()
    conn.close()
    return render_template('transporte.html', registros=registros)

@app.route('/personas')
def personas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM datos_personas")
    personas = cursor.fetchall()
    conn.close()
    return render_template('personas.html', personas=personas) 

# CRUD/Agregar
@app.route('/transporte/add', methods=['POST'])
def add_transporte():
    guia = request.form['guia']
    telefono = request.form['telefono']
    personas = request.form['personas']
    destino = request.form['destino']
    tiempo = request.form['tiempo']

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO transporte (guia, telefono, personas, destino, tiempo) VALUES (%s, %s, %s, %s, %s)",
                       (guia, telefono, personas, destino, tiempo))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error: {e}")  
        return jsonify({'success': False})
    finally:
        conn.close()

#Registro de personas
@app.route('/personas/add', methods=['POST'])
def add_persona():
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    edad = request.form['edad']
    fecha_de_nacimiento = request.form['fecha_de_nacimiento']
    genero = request.form['genero']

    conn= get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO datos_personas (nombres, apellidos, edad, fecha_de_nacimiento, genero) VALUES (%s, %s, %s, %s, %s)",
                        (nombres, apellidos, edad, fecha_de_nacimiento, genero))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False})
    finally:
        conn.close()

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))
        
# Autenticacion y CRUD Transporte 
@app.route('/transporte/delete/<int:id>', methods=['POST'])
def delete_transporte(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transporte WHERE id = %s", (id,))
    conn.commit()
    conn.close()

    return jsonify(success=True), 200

# Autenticacion y CRUD Personas 
@app.route('/personas/delete/<int:id>', methods=['POST'])
def delete_persona(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datos_personas WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    
    return jsonify(success=True), 200

# Editar
@app.route('/transporte/edit/<int:id>', methods=['GET', 'POST'])
def edit_transporte(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        guia = request.form['guia']
        telefono = request.form['telefono']
        personas = request.form['personas']
        destino = request.form['destino']
        tiempo = request.form['tiempo']
        cursor.execute("UPDATE transporte SET guia = %s, telefono = %s, personas = %s, destino = %s, tiempo = %s WHERE id = %s", 
                       (guia, telefono, personas, destino, tiempo, id))

        conn.commit()
        conn.close()
        flash("Registro actualizado", "success")
        return redirect(url_for('transporte'))
    
    cursor.execute("SELECT * FROM transporte WHERE id = %s", (id,))
    registro = cursor.fetchone()
    conn.close()
    return render_template('edit_transporte.html', registro=registro)

@app.route('/personas/edit/<int:id>', methods=['GET', 'POST'])
def edit_persona(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        edad = request.form['edad']
        fecha_nacimiento = request.form['fecha_de_nacimiento']
        genero = request.form['genero']

        cursor.execute(
            "UPDATE datos_personas SET nombres = %s, apellidos = %s, edad = %s, fecha_de_nacimiento = %s, genero = %s WHERE id = %s",
            (nombres, apellidos, edad, fecha_nacimiento, genero, id)
        )
        conn.commit()
        conn.close()
        flash("Registro actualizado", "success")
        return redirect(url_for('personas'))
    
    cursor.execute("SELECT * FROM datos_personas WHERE id = %s", (id,))
    persona = cursor.fetchone()
    conn.close()
    return render_template('edit_persona.html', persona=persona)

# Buscar Transporte
@app.route('/transporte/search', methods=['POST'])
def search_transporte():
    keyword = request.form['keyword']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM transporte WHERE guia LIKE %s OR destino LIKE %s"
    cursor.execute(query, (f'%{keyword}%', f'%{keyword}%'))
    registros = cursor.fetchall()
    conn.close()
    return render_template('transporte.html', registros=registros)

# Buscar Personas
@app.route('/personas/search', methods=['POST'])
def search_persona():
    keyword = request.form['keyword']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM datos_personas WHERE nombres LIKE %s OR apellidos LIKE %s"
    cursor.execute(query, (f'%{keyword}%', f'%{keyword}%'))
    personas = cursor.fetchall()
    conn.close()
    return render_template('personas.html', personas=personas)

#Chatbot
@app.route('/chat_bot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/respuesta')
def respuesta():
    consulta = request.args.get('query', '').strip()
    consulta_normalizada = normalizar(consulta)

    # Validacion si la consulta coincide con alguna palabra clave
    respuesta_encontrada = None
    for lugar, description in lugares_turisticos.items():
        if normalizar(lugar) in consulta_normalizada: 
            respuesta_encontrada = description
            break

    if respuesta_encontrada:
        return respuesta_encontrada
    else:
        return ("No tengo informacion sobre ese lugar. ¿Te gustaría buscar otro sitio?")

# Vistas
@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route("/miradores")
def miradores():
    return render_template("miradores.html")

@app.route("/playas")
def playas():
    return render_template("playas.html")

@app.route("/balnearios")
def balnearios():
    return render_template("balnearios.html")

@app.route("/senderismo")
def senderismo():
    return render_template("senderismo.html")

@app.route("/plazas")
def plazas():
    return render_template("plazas.html")

@app.route("/hoteles")
def hoteles():
    return render_template("hoteles.html")

@app.route("/restaurantes")
def restaurantes():
    return render_template("restaurantes.html")

@app.route("/comida")
def comida(): 
    return render_template("comida.html")

@app.route("/centros")
def centros(): 
    return render_template("centros.html")



if __name__ == '__main__':
    app.run(debug=True)
