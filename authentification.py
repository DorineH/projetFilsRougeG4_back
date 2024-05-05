from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
# from addUsers import register_user
import json

app = Flask(__name__, template_folder='Templates')
app.config['SECRET_KEY'] = 'Y1EcJXSDSEryUwSpmFet' 

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
    with open('dataBase/users.json', 'r') as f:    
        users = json.load(f)
        for key, user_data in users.items():
            if user_data['username'] == username:
                user = User(username, user_data['password'])        
                user.id = key
                return user
        return None

# Charger un utilisateur depuis l'ID
@login_manager.user_loader
def load_user_by_id(user_id):
    return load_user(user_id)

# Formulaire de connexion
class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[InputRequired()])
    password = PasswordField('Mot de passe', validators=[InputRequired()])
    submit = SubmitField('Connexion')

# Page de connexion
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = load_user(username)
        if user is not None:
            if user.password == password or user.username == username:
                login_user(user)
                return redirect(url_for('protected'))
            else:
                return '<h1>Identifiants invalides2</h1>'
        else: 
            return '<h1>Cet utilisateur n\'existe pas<h1>'
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

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     register_user()
#     return redirect(url_for('register'))

if __name__ == '__main__':
    app.run(debug=True)