#CST 311: Intro to Computer Networks
#Spring 2020A
#Programming Assignment #1
#TCPClient.py

#Amir-Andy Alameddine
#Michael Lee
#Ramon Lucindo
#Sergio Quiroz

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
