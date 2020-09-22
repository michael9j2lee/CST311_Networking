# CST 311: Intro to Computer Networks
# Spring 2020A
# Programming Assignment #1
# TCPServer.py

# Amir-Andy Alameddine
# Michael Lee
# Ramon Lucindo
# Sergio Quiroz

# Import the socket module
from socket import *

# Specify the server port that will be used for the connection
serverPort = 12000

# Create the server sock. AF_INET: underlying network is using IPv4
serverSocket = socket(AF_INET, SOCK_STREAM)

# We associate the server port with this socket
serverSocket.bind(('', serverPort))

# This will trigger listening to any connection requests
serverSocket.listen(1)

# A message to let us know things are ready!
print('The server is ready to receive')

# Continually receive on this port/socket while this program runs
while True:
    # Accept any incoming connections, get specific connect socket for this
    # connection
    connectionSocket, addr = serverSocket.accept()
    # Take our sentence and uppercase it
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    # Send back the updated sentence and close the connection
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()
