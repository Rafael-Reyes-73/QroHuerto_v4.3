import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import mysql.connector
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config.from_object(Config)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB máximo

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

import re
from flask import flash, redirect, url_for, request

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

@app.route('/', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        apodo = request.form.get('usuario', '').strip()
        password = request.form.get('password', '').strip()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE apodo = %s AND estado = 1", (apodo,))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario and check_password_hash(usuario['password'], password):
            session['admin'] = usuario['id']
            return redirect(url_for('QroDash'))

        flash('Usuario o contraseña incorrectos', 'error')
        return redirect(url_for('login_admin'))

    return render_template('Dashlogin.html')




@app.route('/QroDash', methods=['GET', 'POST'])
def QroDash():

    # --- Verificar que haya sesión admin ---
    if 'admin' not in session:
        return redirect(url_for('login_admin'))

    if request.method == 'POST':

        nombre = request.form.get('nombre', '').strip()
        apellido_paterno = request.form.get('apellido_paterno', '').strip()
        apellido_materno = request.form.get('apellido_materno', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        municipio = request.form.get('municipio', '').strip()
        apodo = request.form.get('apodo', '').strip()
        foto = request.files.get('foto_perfil')

        # ---- VALIDACIONES ----
        if not nombre:
            flash('El nombre es obligatorio.', 'danger')
            return redirect(request.url)

        if not apellido_paterno:
            flash('El apellido paterno es obligatorio.', 'danger')
            return redirect(request.url)

        if not apellido_materno:
            flash('El apellido materno es obligatorio.', 'danger')
            return redirect(request.url)

        if not email or not EMAIL_REGEX.match(email):
            flash('Debe ingresar un correo válido.', 'danger')
            return redirect(request.url)

        if not password or len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
            return redirect(request.url)

        if not municipio:
            flash('El municipio es obligatorio.', 'danger')
            return redirect(request.url)

        if not apodo or len(apodo) < 3:
            flash('El apodo debe tener al menos 3 caracteres.', 'danger')
            return redirect(request.url)

        if not foto:
            flash('Debe subir una foto.', 'danger')
            return redirect(request.url)

        if not allowed_file(foto.filename):
            flash('Formato de imagen no permitido.', 'danger')
            return redirect(request.url)

        # --- VALIDACIÓN DE CORREO/APODO EXISTENTE ---
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM usuarios WHERE email = %s OR apodo = %s", (email, apodo))
        existente = cursor.fetchone()

        if existente:
            flash('El correo o el apodo ya están registrados.', 'danger')
            cursor.close()
            conn.close()
            return redirect(request.url)

        cursor.close()
        conn.close()

        # ---- GUARDAR IMAGEN ----
        filename = secure_filename(foto.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # ---- GUARDAR EN BD ----
        conn = get_db_connection()
        cursor = conn.cursor()
        hashed_password = generate_password_hash(password)

        query = """
            INSERT INTO usuarios 
            (nombre, apellido_paterno, apellido_materno, email, password, municipio, apodo, foto_perfil, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)
        """
        cursor.execute(query, (nombre, apellido_paterno, apellido_materno, email, hashed_password, municipio, apodo, filename))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('QroDash'))


    # GET   
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
    total = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total_activos FROM usuarios WHERE estado = 1")
    total_activos = cursor.fetchone()['total_activos']

    cursor.execute("SELECT COUNT(*) AS total_inactivos FROM usuarios WHERE estado = 0")
    total_inactivos = cursor.fetchone()['total_inactivos']

    cursor.execute("SELECT * FROM usuarios WHERE estado = 1")
    usuarios = cursor.fetchall()

    cursor.execute("SELECT * FROM contenido ORDER BY id ASC")
    contenidos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('QroDash.html',
                           usuarios=usuarios,
                           contenidos=contenidos,
                           total=total,
                           total_activos=total_activos,
                           total_inactivos=total_inactivos)




@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET estado = 0 WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Usuario eliminado (desactivado) correctamente', 'success')
    return redirect(url_for('QroDash'))



@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        email = request.form['email']
        municipio = request.form['municipio']
        apodo = request.form['apodo']

        # Foto (opcional)
        foto = request.files.get('foto_perfil')
        filename = None

        # Si subieron nueva foto válida
        if foto and allowed_file(foto.filename):
            filename = secure_filename(foto.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Actualizar datos
        if filename:
            query = """
                UPDATE usuarios SET nombre=%s, apellido_paterno=%s, apellido_materno=%s, email=%s, municipio=%s, apodo=%s, foto_perfil=%s
                WHERE id=%s
            """
            params = (nombre, apellido_paterno, apellido_materno, email, municipio, apodo, filename, id)
        else:
            query = """
                UPDATE usuarios SET nombre=%s, apellido_paterno=%s, apellido_materno=%s, email=%s, municipio=%s, apodo=%s
                WHERE id=%s
            """
            params = (nombre, apellido_paterno, apellido_materno, email, municipio, apodo, id)

        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('QroDash'))

    # cargar datos para mostrar en formulario
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if not usuario:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('QroDash'))

    return render_template('editar_usuario.html', usuario=usuario)


@app.route('/contenido', methods=['GET', 'POST'])
def contenido():
    if request.method == 'POST':
        try:
            slider = request.form['slider']
            titulo_inicial = request.form['titulo_inicial']
            conector = request.form.get('conector', '')
            titulo_final = request.form.get('titulo_final', '')
            anuncio = request.form.get('anuncio', '')
            notas = request.form.get('notas', '')

            imagen_file = request.files.get('imagen')
            if not imagen_file:
                flash('No se envió imagen', 'error')
                return redirect(request.url)

            if not allowed_file(imagen_file.filename):
                flash('Formato de imagen no permitido', 'error')
                return redirect(request.url)

            filename = secure_filename(imagen_file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen_file.save(imagen_path)

            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO contenido (slider, titulo_inicial, conector, titulo_final, anuncio, notas, imagen)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (slider, titulo_inicial, conector, titulo_final, anuncio, notas, filename))
            conn.commit()
            cursor.close()
            conn.close()

            flash('Contenido agregado correctamente', 'success')
            return redirect(url_for('contenido'))
        except Exception as e:
            flash(f'Error al guardar contenido: {e}', 'error')
            return redirect(request.url)

    # GET
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contenido ORDER BY id ASC")
    contenidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('QroDash.html', contenidos=contenidos)

@app.route('/contenido/eliminar/<int:id>', methods=['POST'])
def eliminar_contenido(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contenido WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Contenido eliminado correctamente', 'success')
    return redirect(url_for('QroDash'))

@app.route('/contenido/editar/<int:id>', methods=['GET', 'POST'])
def editar_contenido(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener el contenido
    cursor.execute("SELECT * FROM contenido WHERE id = %s", (id,))
    contenido = cursor.fetchone()

    if not contenido:
        flash('Contenido no encontrado', 'error')
        return redirect(url_for('QroDash'))

    if request.method == 'POST':
        slider = request.form['slider']
        titulo_inicial = request.form['titulo_inicial']
        conector = request.form.get('conector', '')
        titulo_final = request.form.get('titulo_final', '')
        anuncio = request.form.get('anuncio', '')
        notas = request.form.get('notas', '')

        # Manejar imagen
        imagen_file = request.files.get('imagen')
        filename = contenido['imagen']  # Mantener la actual si no suben nueva

        if imagen_file and allowed_file(imagen_file.filename):
            filename = secure_filename(imagen_file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            imagen_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Actualizar en BD
        cursor.execute("""
            UPDATE contenido
            SET slider=%s, titulo_inicial=%s, conector=%s, titulo_final=%s,
                anuncio=%s, notas=%s, imagen=%s
            WHERE id=%s
        """, (slider, titulo_inicial, conector, titulo_final, anuncio, notas, filename, id))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Contenido actualizado correctamente', 'success')
        return redirect(url_for('QroDash'))

    cursor.close()
    conn.close()
    return render_template('editar_contenido.html', contenido=contenido)



#-----------------------------------------------------------------------------------------

@app.route('/intro')
def intro():
    return render_template('intro.html')  # Video de bienvenida

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    # Si ya hay sesión, redirigir al dashboard
    if 'usuario' in session:
        return redirect(url_for('loading'))

    if request.method == 'POST':
        # Detectar si es registro (el modal envía 'nombre')
        if 'nombre' in request.form:
            # --- Lógica de registro ---
            nombre = request.form.get('nombre', '').strip()
            apellido_paterno = request.form.get('apellido_paterno', '').strip()
            apellido_materno = request.form.get('apellido_materno', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            municipio = request.form.get('municipio', '').strip()
            apodo = request.form.get('apodo', '').strip()
            foto = request.files.get('foto_perfil')

            # Validaciones básicas
            if not nombre or not apellido_paterno or not apellido_materno:
                flash('Debe completar todos los campos de nombre.', 'error')
                return redirect(url_for('login'))
            if not email or not EMAIL_REGEX.match(email):
                flash('Debe ingresar un correo válido.', 'error')
                return redirect(url_for('login'))
            if not password or len(password) < 6:
                flash('Contraseña mínima 6 caracteres.', 'error')
                return redirect(url_for('login'))
            if not municipio:
                flash('Debe seleccionar un municipio.', 'error')
                return redirect(url_for('login'))
            if not apodo or len(apodo) < 3:
                flash('Apodo mínimo 3 caracteres.', 'error')
                return redirect(url_for('login'))
            if not foto or not allowed_file(foto.filename):
                flash('Debe subir una foto válida.', 'error')
                return redirect(url_for('login'))

            # Guardar imagen
            filename = secure_filename(foto.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Guardar en DB
            conn = get_db_connection()
            cursor = conn.cursor()
            hashed_password = generate_password_hash(password)
            query = """
                INSERT INTO usuarios 
                (nombre, apellido_paterno, apellido_materno, email, password, municipio, apodo, foto_perfil, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)
            """
            cursor.execute(query, (nombre, apellido_paterno, apellido_materno, email, hashed_password, municipio, apodo, filename))
            conn.commit()
            cursor.close()
            conn.close()

            flash('Usuario registrado con éxito.', 'success')
            return redirect(url_for('login'))

        else:
            # --- Lógica de login ---
            apodo = request.form.get('apodo', '').strip()
            password = request.form.get('password', '')

            if not apodo or not password:
                flash('Debe ingresar apodo y contraseña.', 'error')
                return redirect(url_for('login'))

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE apodo=%s AND estado=1", (apodo,))
            usuario = cursor.fetchone()
            cursor.close()
            conn.close()

            if usuario and check_password_hash(usuario['password'], password):
                session['usuario'] = usuario['id']
                return redirect(url_for('loading'))
            else:
                flash('Apodo o contraseña incorrectos.', 'error')
                return redirect(url_for('login'))

    return render_template('login.html')




@app.route('/loading')
def loading():
    if 'usuario' not in session:
        return redirect(url_for('login'))  # Evita acceso directo sin login
    return render_template('loading.html')

@app.route('/QroHuerto')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario_id = session['usuario']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Traer elementos para el slider
    cursor.execute("SELECT * FROM contenido ORDER BY id ASC")
    slider_items = cursor.fetchall()

    # Traer usuarios activos
    cursor.execute("SELECT * FROM usuarios WHERE estado = 1")
    usuarios = cursor.fetchall()

    # Traer solo apodo y foto del usuario logueado
    cursor.execute("SELECT apodo, foto_perfil FROM usuarios WHERE id = %s", (usuario_id,))
    usuario_data = cursor.fetchone()

    apodo = usuario_data['apodo'] if usuario_data else None
    foto_perfil = usuario_data['foto_perfil'] if usuario_data and usuario_data['foto_perfil'] else None

    cursor.close()
    conn.close()

    return render_template(
        'index.html',
        slider_items=slider_items,
        usuarios=usuarios,
        apodo=apodo,
        foto_perfil=foto_perfil
    )

@app.route('/QroHuerto2')
def index2():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario_id = session['usuario']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Traer elementos para el slider
    cursor.execute("SELECT * FROM contenido ORDER BY id ASC")
    slider_items = cursor.fetchall()

    # Traer usuarios activos
    cursor.execute("SELECT * FROM usuarios WHERE estado = 1")
    usuarios = cursor.fetchall()

    # Traer solo apodo y foto del usuario logueado
    cursor.execute("SELECT apodo, foto_perfil FROM usuarios WHERE id = %s", (usuario_id,))
    usuario_data = cursor.fetchone()

    apodo = usuario_data['apodo'] if usuario_data else None
    foto_perfil = usuario_data['foto_perfil'] if usuario_data and usuario_data['foto_perfil'] else None

    cursor.close()
    conn.close()

    return render_template(
        'QroHuerto.html',
        slider_items=slider_items,
        usuarios=usuarios,
        apodo=apodo,
        foto_perfil=foto_perfil, active_page='index'
    )
    
@app.route('/QroPlay')
def qroplay():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT apodo, foto_perfil FROM usuarios WHERE id = %s", (session['usuario'],))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('QroPlay.html', apodo=usuario['apodo'], foto_perfil=usuario['foto_perfil'])

@app.route('/QroPlayLogin')
def qroplaylogin():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT apodo, foto_perfil FROM usuarios WHERE id = %s", (session['usuario'],))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('QroPlayLogin.html', apodo=usuario['apodo'], foto_perfil=usuario['foto_perfil'])


@app.route('/Test')
def test():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT apodo, foto_perfil FROM usuarios WHERE id = %s", (session['usuario'],))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('Test.html', apodo=usuario['apodo'], foto_perfil=usuario['foto_perfil'],active_page='test')


@app.route('/Catalogo')
def catalogo():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT apodo, foto_perfil FROM usuarios WHERE id = %s", (session['usuario'],))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('Catalogo.html', apodo=usuario['apodo'], foto_perfil=usuario['foto_perfil'], active_page='catalogo')


@app.route('/Resultados')
def resultados():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT apodo, foto_perfil FROM usuarios WHERE id = %s", (session['usuario'],))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        'Resultados.html',
        apodo=usuario['apodo'],
        foto_perfil=usuario['foto_perfil'],
        active_page='resultados'
    )


@app.route('/Ubicacion')
def ubicacion():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT apodo, foto_perfil FROM usuarios WHERE id = %s", (session['usuario'],))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('Ubicacion.html', apodo=usuario['apodo'], foto_perfil=usuario['foto_perfil'], active_page='ubicacion')


@app.route('/Nosotros')
def nosotros():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT apodo, foto_perfil FROM usuarios WHERE id = %s", (session['usuario'],))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('Nosotros.html', apodo=usuario['apodo'], foto_perfil=usuario['foto_perfil'], active_page='nosotros')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(port=3000, debug=True)
