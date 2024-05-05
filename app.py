import warnings
import database
# from flask_session import Session
from flask import Flask, jsonify, request
from utils.passwordHash import hash_password, check_password
from utils.passwordSecure import password_secure
from flask_cors import CORS

warnings.filterwarnings("ignore")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Y1EcJXSDSEryUwSpmFet' 
CORS(app)
# server_session = Session(app)

items = []

@app.route("/")
def hello_world():
    return "Hello World !!!"

# fonctionne correctement
@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    database.getUsers()
    result = database.resultsExportUsers

    return jsonify({'item': result}), 201

# fonctionne correctement
@app.route('/api/v1.0/user/<string:pseudo>', methods=['GET'])
def get_user_by_pseudo(pseudo):
    result = database.get_user_by_pseudo(pseudo)
    if result: 
        return jsonify({'item': result}), 201
    else: 
        return jsonify({'message': 'Utilisateur non trouvé'}), 404

# fonctionne correctement
# création d'un utilisateur
@app.route('/api/v1.0/signup', methods=['POST'])
def signup_user():
    firstName = request.json["prenom"]
    lastName = request.json["nom"]
    pseudo = request.json["pseudo"]
    password = request.json["password"]

    if not (pseudo and password):
            return jsonify({'error': 'Unauthorized', 'message': 'Tous les champs sont obligatoires !'}), 400
        
    if not password_secure(password):
        return jsonify({'error': 'Unauthorized', 'message': 'Mot de passe non sécurisé !'}), 400
        
    existing_user = database.get_user_by_pseudo(pseudo)
    if existing_user:
        return jsonify({'error': 'Unauthorized', 'message': 'Ce pseudo d\'utilisateur existe déjà !'}), 400
        
    hashed_password = hash_password(password)
    user_data = {
        'prenom': firstName,
        'nom': lastName,
        'pseudo': pseudo,
        'password': hashed_password
    }

    database.createUser(user_data)
    print('user added', user_data)
    return f'<h1>Bienvenue nouveau joueur !!</h1>' 

# fonctionne correctement
# connection d'un utilisateur 
@app.route('/api/v1.0/login', methods=['POST'])
def login_user():
    data = request.get_json() #  {password: 'passwordDodo!13', pseudo: 'DodoTheBest'}
    prenom = data.get('prenom')
    pseudo = data.get('pseudo')
    password = data.get('password')
    print('ggggggggggggggggggggg')
    print(data)
    print(prenom)

    # Validation des entrées
    if not data or 'pseudo' not in data or 'password' not in data:
        return jsonify({'error': 'Unauthorized', 'message': 'Nom ou mot de passe sont requis'}), 400
    
    pseudo = data['pseudo']
    password = data['password']

    user = database.get_user_by_pseudo(pseudo)
    print('jjjjjjjjjjjjjjj')
    print(user) # {'prenom': 'Dorine', 'nom': 'Henry', 'pseudo': 'DodoTheBest', 'password': '$2b$12$DVyIaHyOn6gjiYBeVM4OI.QM0GPvmNZGrclcGAnBuUgywUaFpPZWS'}

    if not user:
        return jsonify({'error': 'Unauthorized', 'message': 'Utilisateur non trouvé'}), 401

    if user and check_password(user['password'], password):
        return jsonify({'message': 'Connexion réussie', 'user': user}), 200
    else:
        return jsonify({'error': 'Unauthorized', 'message': 'Nom ou mot de passe incorrect'}), 401

# fonctionne correctement
# @app.route('/api/v1.0/users', methods=['POST'])
# def create_user():
#     data = request.json
#     database.createUser(data)
#     return jsonify({'item': 'User created !'}), 201

if __name__ == '__main__':
    app.run(debug=True)