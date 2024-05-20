from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

users = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    users.append(username)
    emit('user_joined', {'username': username}, broadcast=True)
    print(f'{username} joined the chat ! ')

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    emit('message', {'username': username, 'message': message}, broadcast=True)
    print(f'{username}: {message}')

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    if username in users:
        users.remove(username)
        emit('user_left', {'username': username}, broadcast=True)
        print(f'{username} left the chat !')

if __name__ == '__main__': 
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
