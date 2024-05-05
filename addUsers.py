from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
from utils.passwordSecure import password_secure
from utils.passwordHash import hash_password, check_password
import json
import database

app = Flask(__name__, template_folder='Templates')
app.config['SECRET_KEY'] = 'Y1EcJXSDSEryUwSpmFet' 

# Fonction pour charger les utilisateurs depuis le fichier JSON
def load_users(username):
    users = database.getUsers(username)
    return users

# Fonction pour enregister les utilisateurs dans le fichier JSON
def users_saved(users):
    with database.getUsers(users) as f:
        json.dump(users, f, indent=4)

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[InputRequired()])
    password = PasswordField('Mot de passe', validators=[InputRequired()])
    submit = SubmitField('Connexion')

# Route pour enregistrer un nouvel utilisateur
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
            
        if not (username and password):
            return jsonify({'message': 'Tous les champs sont obligatoires !'}), 400
    
        users = load_users()
        for user_id, user in users.items():
            if user['username'] == username:
                return '<h1>Ce nom d\'utilisateur existe déjà !</h1>'

        if (password_secure(password) == True):
            hashed_password = hash_password(password)
            user_id = str(len(users) + 1) 
            user = {
                'username': username,
                'password': hashed_password
            }    

            users[user_id] = user
            users_saved(users)
            return redirect(url_for('connection'))
    return render_template('register.html', form=form)

@app.route('/connection', methods=['GET'])
def connection():
    return f'<h1>Bienvenue nouveau gamer !</h1>' 

if __name__ == '__main__':
    app.run(debug=True)