# CST 311
# Programming Assignment 2
# Team 7
# Amir-Andy Alameddine
# Michael Lee
# Ramon Lucindo
# Sergio Quiroz

# UDPPingerClient.py

# Import socket module and import all of its contents, subprocess and re
from socket import *
import subprocess
import re

#Holds the name of the server's host name
serverName = 'localhost'
#Specify the Server Port Number
serverPort = 12000

#Create client socket.  AF_INET: underlying network is using IPv4
#SOCK_DGRAM: UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
#Gets the user's input and stores url
url = input('Enter url you want to ping : ')
# Start Pinging
ping = subprocess.Popen (
    ["ping", url],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)
output, error = ping.communicate()
# Search entire string
exp = re.search('(\d+\.\d+\.\d+\.\d+)', output)
ip = exp.group(0)
#Encodes the message into bytes and sends the message through the socket
#It also sends it to the server by specifying the server's hostname and port
#number to send it to
clientSocket.sendto(output.encode(),(serverName, serverPort))
#Gets the modified message from server (received from port 1024)
modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
#Decodes message and prints it
print(modifiedMessage.decode())
#Closes the socket after the message is received
clientSocket.close()
