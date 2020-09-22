#CST 311: Intro to Computer Networks
#Spring 2020A
#Programming Assignment #1

#Amir-Andy Alameddine
#Michael Lee
#Ramon Lucindo
#Sergio Quiroz

#UDPServer.py

#Import the module socket and all the contents
from socket import *

#Specify the Server Port Number
serverPort = 12000

#Create server socket.  AF_INET: underlying network is using IPv4
#SOCK_DGRAM: UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

#Any packet sent to port number 12000 will be directed to this socket
serverSocket.bind(('', serverPort))

print('The server is ready to receive')

#While the program is running, make sure to continually receive on this
#port/socket
while True:
	#Packet data put into message
	#clientAddress holds the client's IP Address
    message, clientAddress = serverSocket.recvfrom(2048)
	#Decodes message and makes it into Upper case.  Stores into modifiedMessage
    modifiedMessage = message.decode().upper()
	#Converts message into bytes and then sends the packet into server's socket
    #Delivers to Client
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)

#UDPClient.py

#Import socket module and import all of its contents
from socket import *
#Holds the name of the server's host name
serverName = 'localhost'
#Specify the Server Port Number
serverPort = 12000

#Create client socket.  AF_INET: underlying network is using IPv4
#SOCK_DGRAM: UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
#Gets the user's input and stores into message
message = input('Input lowercase sentence:')
#Encodes the message into bytes and sends the message through the socket
#It also sends it to the server by specifying the server's hostname and port
#number to send it to
clientSocket.sendto(message.encode(),(serverName, serverPort))
#Gets the modified message from server (received from port 2048)
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
#Decodes message and prints it
print(modifiedMessage.decode())
#Closes the socket after the message is received
clientSocket.close()

# TCPServer.py

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

#TCPClient.py

#Import socket module and import all of its contents
from socket import *
#Holds the name of the server's host name
serverName = '10.0.0.2'
#Specify the Server Port Number
serverPort = 12000

#creates client socket. Para 1.indicates IPv4 2.indicates it is a TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)
#TCP connection is established between client and server
clientSocket.connect((serverName, serverPort))
#Obtains a sentence from the user
sentence = input('Input lowercase sentence:')
#The line sends to client's socket by dropping the sentence into bytes into the TCP conn
clientSocket.send(sentence.encode())
#The client's socket is closed after the all the string is completed
modifiedSentence = clientSocket.recv(1024)
#Decodes modifiedSentence and prints it
print('From Server: ', modifiedSentence.decode())
#Closes the socket after the message is received. TCP in the client sends TCP message to TCP in the server
clientSocket.close()
