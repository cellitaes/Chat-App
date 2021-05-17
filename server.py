#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import threading
import socket

HOST = 'localhost'
PORT = 33000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def receive():
    while True:
        client, address = server.accept()
        print(client)
        print(f"Connected with {str(address)}")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        for nick in nicknames:
            client.send(f"UPDATE JOIN {nick}".encode('utf-8'))

        print(nickname)
        broadcast(f"UPDATE JOIN {nickname}".encode('utf-8'))

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is: {nickname}")
        broadcast(f"{nickname} has just connected to the server\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} has just left the chat\n".encode('utf-8'))
            nicknames.remove(nickname)
            broadcast(f"UPDATE LEFT {nickname}".encode('utf-8'))
            break


print("Waiting for the connections...")
receive()
