import threading

import socket


host = '127.0.0.1' #localhost

port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) #binding host and port
server.listen() #puts our server into listening mode for new connections

clients = [] #clients list, new clients will go into here.
nicknames = [] #nicknames list, nicknames will be stored here.


#Defining 3 methods

#First method. Function that send a message to all the clients that are connected to the server.

def broadcast(message):
    for client in clients:
        client.send(message)

#Second method. We are handling the clients connection, receiving and sending messages. 

def handle(client):
    while True:
        try:
            message = client.recv(1024) #we receive the message and we broadcast it to the whole room, with a max length of 1024 bytes
            broadcast(message)
        except: #if there is an error in receiving the message, we cut the connection with this client.
            index = clients.index(client) #find the client in the loop
            clients.remove(client) #remove him from the list
            client.close() #close connection with him
            nickname = nicknames[index] #find the nickname
            broadcast(f'{nickname} left the chat!'.encode('ascii')) #broadcast that the client left
            nicknames.remove(nickname) #remove the nickname from the list
            break #stop the loop

#Main method, main functionlity of the client handling.

def receive():
    while True:
        client, address = server.accept() #accepting clients all the time
        print(f"Connected with {str(address)}") #when the client connects we send him the address in which he is connected

        client.send('NICK'.encode('ascii')) #we send this code word so the client will send his nickname
        nickname = client.recv(1024).decode('ascii') #we receive this nickname
        clients.append(client) #we append the name to the array of clients

        print(f'Nickname of the client is {nickname}!') #we print the name of the new client connected
        broadcast(f'{nickname} joined the chat!'.encode('ascii')) #we are gonna broadcast to all the members of the chat room that this client is connected
        client.send('Connected to the server'.encode('ascii')) #we are gonna send this new client that the connection was successful

        thread = threading.Thread(target=handle, args=(client,)) #defining threads. One thread for each client.
        thread.start()


print("Server is listening...")

receive()