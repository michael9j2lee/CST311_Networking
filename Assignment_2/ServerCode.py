from socket import *
import random
import time

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('', 12000))

while True:
        # Generate random number in the range of 0 to 10
        rand = random.randint(0, 10)
        print ("random number is ", rand)
        # Receive the client packet along with the address it is coming from
        message, address = serverSocket.recvfrom(1024)
        # Capitalize the message from the client
        message = message.upper()
        # If rand is less is than 4, we consider the packet lost and do not respond
        if rand < 4:
            print ("Packet is lost ")
            continue
        #Test for timeout by setting this higher
        time.sleep(.5)
        # Otherwise, the server responds
        serverSocket.sendto(message, address)
