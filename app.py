import warnings
import database
import subprocess
import dataBaseMongoDb
# import pygame

# from flask_session import Session
from flask import Flask, jsonify, request
from utils.passwordHash import hash_password, check_password
from utils.passwordSecure import password_secure
from flask_cors import CORS
from flask_socketio import SocketIO, send

warnings.filterwarnings("ignore")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Y1EcJXSDSEryUwSpmFet' 
CORS(app)

socketIo = SocketIO(app, cors_allowed_origins="*")

# server_session = Session(app)

items = []

@app.route("/")
def hello_world():
    return "Hello World !!!"

# récuper les users (mongoDB OK)
@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    # database.getUsers()
    # result = database.resultsExportUsers
    dataBaseMongoDb.getUsersMongoDB()
    result = dataBaseMongoDb.resultsExportUsers

    return jsonify({'users': result}), 201

# récupere un user en fonction de son pseudo (mongoDB OK)
@app.route('/api/v1.0/user/<string:pseudo>', methods=['GET'])
def get_user_by_pseudo(pseudo):
    # result = database.get_user_by_pseudo(pseudo)
    result = dataBaseMongoDb.getUserByPseudo(pseudo)
    if result: 
        return jsonify({'user': result}), 201
    else: 
        return jsonify({'message': 'Utilisateur non trouvé'}), 404

# Création d'un utilisateur (mongoDB OK)
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
        
    # existing_user = database.get_user_by_pseudo(pseudo)
    existing_user = dataBaseMongoDb.getUserByPseudo(pseudo)
    if existing_user:
        return jsonify({'error': 'Unauthorized', 'message': 'Ce pseudo d\'utilisateur existe déjà !'}), 400
        
    hashed_password = hash_password(password)
    user_data = {
        'prenom': firstName,
        'nom': lastName,
        'pseudo': pseudo,
        'password': hashed_password
    }

    # database.createUser(user_data)
    dataBaseMongoDb.createUserMongoDB(user_data)
    print('user added', user_data)
    return f'<h1>Bienvenue nouveau joueur !!</h1>' 

# Connection d'un utilisateur (mongoDB OK)
@app.route('/api/v1.0/login', methods=['POST'])
def login_user():
    data = request.get_json() #  {password: 'passwordDodo!13', pseudo: 'DodoTheBest'}
    prenom = data.get('prenom')
    pseudo = data.get('pseudo')
    password = data.get('password')

    # Validation des entrées
    if not data or 'pseudo' not in data or 'password' not in data:
        return jsonify({'error': 'Unauthorized', 'message': 'Nom ou mot de passe sont requis'}), 400
    
    pseudo = data['pseudo']
    password = data['password']

    # user = database.get_user_by_pseudo(pseudo)
    user = dataBaseMongoDb.getUserByPseudo(pseudo)
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

# fonctionne du jeu snake 
@app.route('/api/v1.0/launchSnake', methods=['GET'])
def launch_snake():
    try:
        subprocess.Popen(["python", "snakeGame.py"])
        return jsonify({"status": "succes", "message": "Snake game launched"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# fonctionne pour enregister le score du joueur
@app.route('/api/v1.0/score', methods=['POST'])
def post_score():
    data = request.get_json()
    pseudo = data.get('pseudo')
    score = data.get('score')

    if not pseudo or not score:
        return jsonify({'error': 'Invalid'}), 400
    
    database.save_score(pseudo, score)

    return jsonify({'status': 'success', 'score_received': score})

# fonction pour récupper les scores
@app.route('/api/v1.0/score/<string:pseudo>', methods=['GET'])
def get_scores_by_by_pseudo(pseudo):
    scores = database.get_scores_by_pseudo(pseudo)
    if scores:
        return jsonify({'scores': scores}), 200
    else:
        return jsonify({'message': 'Aucun score trouvé pour cet utilisateur'}), 404
    
@socketIo.on("message")
def handleMessage(msg):
    print(msg)
    send(msg, broadcast=True)
    return None

if __name__ == '__main__':
    socketIo.run(app, debug=True)