from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Active CORS pour toutes les routes de l'application

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from the back !!"}
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.json
    response = {"received": data}
    return jsonify(response)

@app.route('/favicon.ico')
def favicon():
    return '', 404

if __name__ == '__main__':
    app.run(debug=True)

