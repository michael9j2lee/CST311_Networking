# CST 311
# Programming Assignment 2
# Team 7
# Amir-Andy Alameddine
# Michael Lee
# Ramon Lucindo
# Sergio Quiroz

# UDPPingerClient.py

#module declaration

import socket
from socket import AF_INET, SOCK_DGRAM
import time

# Declare UDP port number
udpPortNumber = 12000
#setting up server (localhost)
udpIPAddress = 'localhost'

# Display the message
print('Pinging', udpIPAddress, udpPortNumber)
#creating socket
clientSocket = socket.socket(AF_INET,SOCK_DGRAM)
#set timeout frome server to 1sec
clientSocket.settimeout(1)
#RTT in array to store value may change
RTT = []
#sequence count
seqCount = 1

baseMessage = "holy cow {}"

while seqCount<= 10:
    #current time
    startTime = time.time()

    # Assign sequence count in the variable named 'message'
    inputMessage = baseMessage.format(seqCount)

    #client sends a message to the server
    clientSocket.sendto(inputMessage.encode('utf-8'), (udpIPAddress, udpPortNumber))
    

    #declaration of try, catch and handle exception
    try:
        #message from server 1204 from udppingerserver.py
        message, address = clientSocket.recvfrom(1024)
        print("GOT MESSAGE", message)
        #time elapsed
        elapsedTime = (time.time() - startTime)

        #RTT roundTripTime adding to array
        RTT.append(elapsedTime)


        print('Ping message number ' + str(seqCount) + ' Round Trip Time(RTT):' + str(elapsedTime) + ' secs')

        #response message from the server
        print(message)

    except socket.timeout:

        #message what packet has been lost due to timeout (usually 1 sec)
        print('Package lost ' + str(seqCount)+' request timed out.')

    seqCount += 1

    print('')
    

    #calculations after the result is over 10
    if seqCount > 10:
        #RTT max
        print('rtt max')

        #RTT min
        print('rtt min')

        #RTT avg
        print('rtt avg')

        #estimated RTT (alpha =.125)
        print('estimated RTT')

        #devRTT (beta = .25) (timout interval)
        print('dev RTT')

        #packetLoss (in percentage)
        print('packet loss %')

        clientSocket.close()




