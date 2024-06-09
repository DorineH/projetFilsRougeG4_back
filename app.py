import warnings
import database
from flask import Flask, jsonify, request

warnings.filterwarnings("ignore")

app = Flask(__name__)

items = []

@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    database.getUsers()
    result = database.resultsExportUsers

    return jsonify({'item': result}), 201


@app.route('/api/v1.0/users', methods=['POST'])
def create_user():
    data = request.json
    database.createUser(data)
    return jsonify({'item': 'User created !'}), 201


if __name__ == '__main__':
    app.run(debug=True)