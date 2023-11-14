from flask import Flask, redirect, render_template, request, url_for,session,flash
from config import *
from user import User
from admin import Admin

# Instancias para realizar operaciones con la DB
con_bd = Conexion()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# Crear usuario
@app.route('/registro')
def registro():
    # Se modifica la vista index para poder hacer el muestreo de los datos
    usuarios = con_bd['Usuarios']
    UsuariosRegistradas=usuarios.find()
    return render_template('registro.html', usuarios = UsuariosRegistradas)


# Ruta para guardar los datos de la DB
@app.route('/guardar_usuarios', methods = ['POST'])
def agregarUser():
    usuarios = con_bd['Usuarios']
    nombre = request.form['nombre']
    email = request.form['email']
    cumple = request.form['cumple']
    password = request.form['password']
    roll=request.form['roll']

    if nombre and email and cumple and password and roll:
        user = User(nombre, email, cumple, password, roll)
        #insert_one para crear un documento en Mongo
        usuarios.insert_one(user.formato_doc())
        return redirect(url_for('registro'))
    else:
        return "Error"

@app.route('/login')
def login():
    # Lógica para mostrar la página de inicio de sesión
    return render_template('login.html')


app.secret_key = 'cronO-UdEc'


#Validación de usuario
@app.route('/validar', methods = ['POST'])
def validar():
    email = request.form['email']
    password = request.form['password']

    usuarios = con_bd['Usuarios']
    user_data = usuarios.find_one({"email": email, "password": password})

    if user_data:
        # Autenticación exitosa, almacenar el usuario en la sesión
        session['usuario'] = email
        return redirect(url_for('inicio'))
    else:
        flash('Error de autenticación, email o Contraseña incorrecta', 'error')
        return redirect(url_for('login'))

@app.route('/inicio')
def inicio():
    actividades = con_bd['Actividades']
    ActividadesRegistradas = actividades.find()
    return render_template('inicio.html', actividades=ActividadesRegistradas)

@app.route('/perfil')
def perfil():
    actividades = con_bd['Actividades']
    # Obtener el nombre del usuario de la sesión
    autor = session.get('usuario')

    if autor:
        # Filtrar las actividades por el nombre del usuario
        ActividadesRegistradas = actividades.find({'autor': autor})
        return render_template('perfil.html', actividades=ActividadesRegistradas)
    else:
        flash('Error: Usuario no autenticado', 'error')
        return redirect(url_for('inicio'))

# Ruta de error 404
def error_404(error):
    return render_template('error_404.html'), 404


# Ruta para guardar los datos de la actividades de la DB
@app.route('/agregarActividad', methods=['POST'])
def agregarActividad():
    actividades = con_bd['Actividades']
    publicacion = request.form['publicacion']
    fecha = request.form['fecha']
    comentario = request.form['comentario']

    # Obtener el nombre del usuario de la sesión
    autor = session.get('usuario')

    if publicacion and autor and fecha and comentario:
        admin = Admin(publicacion, autor, fecha, comentario)
        # insert_one para crear un documento en Mongo
        actividades.insert_one(admin.formato_doc())
        return redirect(url_for('inicio'))
    else:
        return "Error"
    

#Editar o actualizar el contenido de la actividad
@app.route('/editar_actividad/<string:actividad_buscada>', methods = ['POST'])
def editar(actividad_buscada):
    actividades = con_bd['Actividades']
    publicacion= request.form['publicacion']
    autor = request.form['autor']
    fecha = request.form['fecha']
    comentario = request.form['comentario']
    # Utilizaremos la función update_one()
    if publicacion and autor and fecha and comentario:
        actividades.update_one({'publicacion': actividad_buscada}, 
                            {'$set': {'publicacion' : publicacion, 'autor': autor, 'fecha' : fecha, 'comentario': comentario}}) # update_one() necesita de al menos dos parametros para funcionar
        return redirect(url_for('inicio'))
    else:
        return "Error de actualización"
    
#Eliminar actividad
@app.route('/eliminar_actividad/<string:actividad_buscada>', methods = ['POST'])
def eliminar(actividad_buscada):
    actividades = con_bd['Actividades']
    # Se hace uso de delete_one para borrar los datos de la DB personas donde el dato que se elimina es el que se para como argumento para nombre
    actividades.delete_one({ 'nombre': actividad_buscada})
    # Creamos un redireccionamiento que redirija a la vista index
    return redirect(url_for('perfil'))

if __name__ == '__main__':
    app.register_error_handler(404, error_404)
    app.run(debug = True, port = 2001)
















    
'''
# En este caso se eliminara atravez de la URL
# Ruta para eliminar datos en la DB donde la ruta se llama eliminar_persona y recibe un parametro llamado nombre_persona
@app.route('/eliminar_usuarios/<string:usuario_user>')
def eliminar(usuario_user):
    usuarios = con_bd['Usuarios']
    # Se hace uso de delete_one para borrar los datos de la DB personas donde el dato que se elimina es el que se para como argumento para nombre
    usuarios.delete_one({ 'usuario': usuario_user})
    # Creamos un redireccionamiento que redirija a la vista index
    return redirect(url_for('registro'))

#Editar o actualizar el contenido 
@app.route('/editar_usuarios/<string:usuario_user>', methods = ['POST'])
def editar(usuario_user):
    usuarios = con_bd['Usuarios']
    # Se realiza el mismo proceso de inserción y extracción para poder actualizar los datos
    usuario = request.form['usuario']
    roll = request.form['roll']
    password = request.form['password']
    # Utilizaremos la función update_one()
    if usuario and roll and password:
        usuarios.update_one({'usuario': usuario_user}, 
                            {'$set': {'usuario' : usuario , 'roll': roll, 'password': password}}) # update_one() necesita de al menos dos parametros para funcionar
        return redirect(url_for('registro'))
    else:
        return "Error de actualización"

'''