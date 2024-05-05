from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
import database
from utils.passwordSecure import password_secure
from utils.passwordHash import hash_password
from utils.passwordHash import check_password
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Y1EcJXSDSEryUwSpmFet' 

bcrypt = Bcrypt(app)

# Configurer Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Classe User
class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.username

# Charger un utilisateur depuis le fichier JSON
def load_user(username):
    users = database.getUserByName(username)
    if users:
        user = User(username=users['name'], password=users['password'])        
        return user
    return None

# Charger un utilisateur depuis l'ID
@login_manager.user_loader
def load_user_by_id(user_id):
    return load_user(user_id)

# Formulaire d'inscription 
class RegisterForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[InputRequired()])
    password = PasswordField('Mot de passe', validators=[InputRequired()])
    submit = SubmitField('Inscription')

# Formulaire de connexion
class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[InputRequired()])
    password = PasswordField('Mot de passe', validators=[InputRequired()])
    submit = SubmitField('Connexion')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if not (username and password):
            return jsonify({'message': 'Tous les champs sont obligatoires !'}), 400
        
        if not password_secure(password):
            return jsonify({'message': 'Mot de passe non sécurisé !'}), 400
        
        existing_user = database.getUserByName(username)
        if existing_user:
            return '<h1>Ce nom d\'utilisateur existe déjà !</h1>'
        
        hashed_password = hash_password(password)
        user_data = {
            'name': username,
            'password': hashed_password
        }

        database.createUser(user_data)
        print('user added', user_data)
        return f'<h1>Bienvenue nouveau joueur !!</h1>' 
    # redirect(url_for('login'))
    return render_template('register.html', form=form)

# Page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = load_user(username)

        if user:
            if check_password(user.password, password):
                login_user(user)
                return redirect(url_for('protected'))
            else:
                return '<h1>Mot de passe incorrect</h1>'
        else:
            return '<h1>Cet utilisateur n\'existe pas</h1>'
    return render_template('login.html', form=form)

# Page protégée, accessible uniquement aux utilisateurs connectés
@app.route('/protected')
@login_required
def protected():
    return f'<h1>Vous êtes connecté en tant que {current_user.username}</h1>' 

# Déconnexion de l'utilisateur
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)