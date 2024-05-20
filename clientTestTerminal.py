import socket
import threading

IP = "127.0.0.1"
PORT = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((IP, PORT))

pseudo = input("Enter your pseudo: ")

client.send(bytes(pseudo, "utf-8"))

# fonction d'envoie de message
def send_message():
    while True:
        message = input()
        client.send(bytes(message, "utf-8"))

        if message == "exit":
            break

def receive_message():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            print(message)

        except:
            break

thread_send = threading.Thread(target=send_message)
thread_reception = threading.Thread(target=receive_message)

thread_send.start()
thread_reception.start()

        