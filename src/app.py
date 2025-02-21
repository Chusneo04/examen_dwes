from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from security import token_hex
#uri = "mongodb+srv://hugoarroyogalle:MhCH24n6dQZMymAF@examen.b655m.mongodb.net/?retryWrites=true&w=majority&appName=Examen"
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/examen'
mongo = PyMongo(app)
print(mongo.db.examen.usuarios.find())



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    try:
        if current_user.isauthenticated:
            return redirect(url_for('perfil'))
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            password = generate_password_hash(password)
            print(username, email, password)

            if not username or not email or not password:

                return render_template('register.html')
            
            usuario=mongo.db.examen.usuarios.find({'email':email})
            if usuario:
                print('El usuario ya existe')
                return render_template('register.html')
            
            mongo.db.examen.usuarios.insert_one({'username':username, 'email':email, 'password':password, 'coches':[]})
            user = {'username': username,'email':email, 'password':password }
            login_user(user)
            return redirect(url_for('login'))

        return render_template('register.html')

    except Exception as e:
        print(e)
        return 'Hola'

@app.route('/login', methods = ['POST', 'GET'])
def login():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            password = check_password_hash(password)
            if not email or not password:
                return render_template('login.html')
        

        return render_template('login.html')
    except Exception as e:
        print(e)

@login_required
@app.route('/crud_update/<id>', methods=['GET', 'POST'])
def crud_añadir(id):
    try:
        if request.method == 'POST':
            foto = request.form.get('imagen')
            descripcion = request.form.get('descripcion')

            if not foto or not descripcion:
                return render_template('crud_añadir.html')
            
            coche = {'foto':foto, 'descripcion':descripcion, 'id_coche':token_hex(24)}
            mongo.db.usuarios.update_one({{'id_coche':id}, {'$set':{'coches':coche}}})
            return redirect(url_for('perfil'))
        return render_template('crud_update')
    except Exception as e:
        print(e)

@login_required
@app.route('/crud_añadir/<id>', methods=['GET', 'POST'])
def crud_añadir(id):
    try:
        if request.method == 'POST':
            foto = request.form.get('imagen')
            descripcion = request.form.get('descripcion')

            if not foto or not descripcion:
                return render_template('crud_añadir.html')
            
            coche = {'foto':foto, 'descripcion':descripcion, 'id_coche':token_hex(24)}
            mongo.db.usuarios.insert_one({'coches':coche})
            return redirect(url_for('perfil'))
        return render_template('crud_añadir.html')
            
    except Exception as e:
        print(e)

@login_required
@app.route('/crud_delete/<id>')
def crud_delete(id):
    try:
        mongo.db.usuarios.delete_one({'coches':{'id':id}})
        return redirect(url_for('crud_añadir'))
    except Exception as e:
        print(e)

@login_required
@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    try:
        usuario = mongo.db.usuarios.find({'id':id})
        coches = usuario['coches']
        return render_template('perfil.html', coches = coches)
    except Exception as e:
        print(e)

@login_required
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('/login'))

@login_required
@app.route('/perfil/admin', methods = ['GET', 'POST'])
def admin():
    if current_user.username != 'admin':
        return redirect(url_for('login'))
    
    usuarios = mongo.db.usuarios.find()
    coches = usuarios['coches']

    return render_template('admin.html', coches = coches, usuarios = usuarios)

if __name__ == '__main__':
    app.run(debug=True)