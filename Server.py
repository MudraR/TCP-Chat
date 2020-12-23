'''
By: Mudra Rawal
Project: TCP Chat
Description: This chatroom consists of a TCP server that tracks usernames, and a client program for the chats. 
'''
import threading
import socket


# server is host

"""
ports range from:
0-1023 -- Well Known
1024-49151 -- Registered
49152-65535 -- Dynamic
"""
port = 50505 #Using dynamic random port -- unused by the public. 
host = '127.0.0.1' #loopback address

# Server Config
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#AF_INET is just IPv4 addresses.
server.bind((host, port))
server.listen()

clients = []
usernames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Handling Leaving Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast('{} left!'.format(username).encode('ascii'))
            usernames.remove(username)
            break
  
# Receiving / Listening Function
def receive():
    while True:
        # Accepting the Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Get the username from client
        client.send('USER'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        # Broadcasting New Users
        print("Username is {}".format(username))
        broadcast("{} joined!".format(username).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Threading between clients
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
