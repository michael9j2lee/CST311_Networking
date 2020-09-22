#CST 311: Intro to Computer Networks
#Spring 2020A
#Programming Assignment #1
#UDPServer.py

#Amir-Andy Alameddine
#Michael Lee
#Ramon Lucindo
#Sergio Quiroz


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
