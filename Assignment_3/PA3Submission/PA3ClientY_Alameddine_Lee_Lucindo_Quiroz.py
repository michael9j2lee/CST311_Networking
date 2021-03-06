# CST 311
# Programming Assignment 3
# Amir-Andy Alameddine
# Michael Lee
# Ramon Lucindo
# Sergio Quiroz
# PA3ClientY_Alameddine_Lee_Lucindo_Quiroz.py

from socket import *
# In your command prompt, type in hostname and press enter.
# What comes up is your computer's hostname
serverName = '127.0.0.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

sentence = 'Client Y: Bob'

clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)

print('Sent to server: ', sentence)
print('From Server:', modifiedSentence.decode())

clientSocket.close()
