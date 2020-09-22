# CST 311
# Programming Assignment 2
# Team 7
# Amir-Andy Alameddine
# Michael Lee
# Ramon Lucindo
# Sergio Quiroz

# UDPPingerServer.py
# We will need the following module to generate randomized lost packets

import random
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets

serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket

serverSocket.bind(('', 12000))
while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    print("random number is " , rand)

    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    # Capitalize the message from the client
    message = message.upper()
# If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4:
        continue
# Otherwise, the server responds
    serverSocket.sendto(message, address)


# UDPPingerClient.py

# module declaration
from socket import *
import time


# UDP Pinger Class
class UDPPingerClient(object):

    # CONSTRUCTOR.  Initialize variables.
    # Params: port number , ipAddress/host
    def __init__(self, portNumber, ipAddress):
        # Initialize variables passed into UDPPingerClient
        self.portNumber = portNumber
        self.ipAddress = ipAddress
        # Initialize variables
        self.max = 0.0
        self.min = 0.0
        self.sum = 0.0
        self.estRTT = 0.0
        self.devRTT = 0.0
        self.lost = 0
        self.timeout = 0.0
        self.message = ''
        self.seqCount = 0
        self.response = ''

        # Initialize alpha/beta
        self.a = .125
        self.b = .25

        # create socket and set timeout
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.settimeout(1)

    # Send the Message
    def sendMessage(self):

        # Start the timer
        start = time.time()
        # Set the message to the current count
        self.message = "hello, this is message #{0}".format(self.seqCount)
        # Initialize current Time
        currRTT = 0
        # Send Message through socket
        self.clientSocket.sendto(self.message.encode('utf-8'), (self.ipAddress, self.portNumber))

        # Try catch for receiving the message.
        try:
            # Received message
            recvMessage, address = self.clientSocket.recvfrom(1024)
            # Get the response
            self.response = recvMessage.decode('utf-8')
            end = time.time()

            # time elapsed
            currRTT = float(round((end - start) * 1000))

        # If a timeout occurs, consider it a loss
        except timeout:
            self.response = '**Packet Lost for {0}**'.format(self.seqCount)
            # print('Package lost ' + str(self.seqCount)+' request timed out.')
            self.lost += 1
            # Set the elapsed time as 1 (Default timeout)
            currRTT = 1000

        # Increment sequence count
        self.seqCount += 1
        # Calculate min and max and stuff
        self.calculateCurrent(currRTT)
        # Print the current time/Reply
        self.printCurrent(currRTT)

    # Calculate the current values (Max, Min, SUM... etc)
    def calculateCurrent(self, currRTT):
        # MIN and MAX
        if currRTT > self.max:
            self.max = currRTT
        if currRTT < self.min:
            self.min = currRTT
        # Get the sum for the average
        self.sum += currRTT
        # Calculate estRTT and devRTT
        self.estRTT = (1 - self.a) * self.estRTT + self.a * currRTT
        self.devRTT = (1 - self.b) * self.devRTT + self.b * abs(currRTT - self.estRTT)

    # Given the estRTT and devRTT, calculate the timeout
    def calculateTimeout(self):
        timeout = self.estRTT + 4 * self.devRTT
        return timeout

    # Prints the current time for the reply
    def printCurrent(self, currTime):
        print("Reply from {0} time = {1}".format(self.ipAddress, currTime))
        print("\testRTT = {0}, devRTT = {1}, message = {2}".format(self.estRTT, self.devRTT, self.response))

    # Get the aggregate counts/statistics of the Ping run
    def printStats(self):
        # Calculate the average with sum and counts
        avg = self.sum / self.seqCount
        # Calculaate the percentage lost with counts of lost and total
        percentLoss = (self.lost / self.seqCount) * 100
        # Calculate the recieived with the total and counts of lost
        received = self.seqCount - self.lost
        # Calculate Timeout with estRTT and devRTT
        timeout = self.calculateTimeout()

        print("Ping statistics for ", self.ipAddress)
        print("\tPackets: Sent = {0}, Received = {1}, Lost = {2} ({3}% loss)".format(self.seqCount, received, self.lost,
                                                                                     percentLoss))
        print("Approximate round trip times")
        print("\tMinimum = {0}, Maximum = {1}, Average = {2}".format(self.min, self.max, avg))
        print("\tTimeout = {0}".format(timeout))

    def closeSocket(self):
        self.clientSocket.close()


# Runs the script
if __name__ == '__main__':
    # Set port and ip address
    portNum = 12000
    ipAdd = '127.0.0.1'
    # Initialize the object
    udpClient = UDPPingerClient(portNum, ipAdd)
    totalCount = 0
    # run this 10 times.
    while totalCount < 10:
        udpClient.sendMessage()
        totalCount += 1
    # print stats and then close socket
    udpClient.printStats()
    udpClient.closeSocket()
