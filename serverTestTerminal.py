from flask import Flask, render_template, request, jsonify
import socket
import threading
import atexit

app = Flask(__name__)

IP = "127.0.0.1"
PORT = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def close_server():
    server.close()

atexit.register(close_server)

try:
    server.bind((IP, PORT))
except OSError as e:
    print(f"Error: {e}")
    exit(1)

server.listen(10)

clients = []
pseudos = []

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    for client in clients:
        # client.send(bytes(message, "utf-8"))
        client.send(message)
    return jsonify({'status': 'OK'})


def connections_management():
    while True:
        client, address = server.accept()
        pseudo = client.recv(1024).decode("utf-8") # permet de recevoir le message
        clients.append(client)
        pseudos.append(pseudo)
        broadcast(f"{pseudo} joined the chat")

        # print(f"Conection establish with {str(adresse)}")
        # client.send(bytes("Welcome on board ! \n", "utf-8"))
        # print(f"{pseudo} joined the chat")

def client_management(client, pseudo):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "exit":
                index = clients.index(client)
                clients.remove(client)
                client.close()
                pseudo = pseudos[index]
                pseudos.remove(pseudo)
                broadcast(f"{pseudo} left the chat")
                break

            else:
                broadcast(f"{pseudo}: {message}")
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            pseudo = pseudos[index]
            pseudos.remove(pseudo)
            broadcast(f"{pseudo} left the chat")
            break

def broadcast(message):
    for client in clients:
        client.send(bytes(message, "utf-8"))


if __name__ == "__main__":
    thread_connections = threading.Thread(target=connections_management)
    thread_connections.start()
    app.run(debug=True)