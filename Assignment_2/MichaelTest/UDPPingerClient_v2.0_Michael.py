# CST 311
# Programming Assignment 2
# Team 7
# Amir-Andy Alameddine
# Michael Lee
# Ramon Lucindo
# Sergio Quiroz

# UDPPingerClient.py

#module declaration
from socket import *
import time


#UDP Pinger Class
class UDPPingerClient(object):

#CONSTRUCTOR.  Initialize variables.
#Params: port number , ipAddress/host
    def __init__ (self, portNumber,ipAddress):
        #Initialize variables passed into UDPPingerClient
        self.portNumber = portNumber
        self.ipAddress = ipAddress
        #Initialize variables
        self.max = 0
        self.min = 0
        self.sum = 0
        self.estRTT = 0
        self.devRTT = 0
        self.lost = 0
        self.timeout = 0
        self.message = ''
        self.seqCount = 0
        
        #Initialize alpha/beta
        self.a = .125
        self.b = .25

        #create socket and set timeout
        self.clientSocket = socket(AF_INET,SOCK_DGRAM)
        self.clientSocket.settimeout(1)

    #Send the Message
    def sendMessage(self):
        #Start the timer
        start = time.time()
        #Set the message to the current count
        self.message = str(self.seqCount)
        #Initialize current Time
        currRTT = 0
        #Send Message through socket
        self.clientSocket.sendto(self.message.encode('utf-8'), (self.ipAddress, self.portNumber))
        
        #Try catch for receiving the message.
        try:
            #Received message
            recvMessage, address = self.clientSocket.recvfrom(1024)
            #print("Got Message", recvMessage)
            end = time.time()

            #time elapsed
            currRTT = (end - start)
            
            #print('Ping message number ' + str(self.seqCount) + ' RTT: ', currRTT)

            #print(recvMessage)

        #If a timeout occurs, consider it a loss
        except timeout:
            #print('Package lost ' + str(self.seqCount)+' request timed out.')
            self.lost +=1
            #Set the elapsed time as 1 (Default timeout)
            currRTT = 1
        
        #Increment sequence count
        self.seqCount+=1
        #Calculate min and max and stuff
        self.calculateCurrent(currRTT)
        #Print the current time/Reply
        self.printCurrent(currRTT)

    #Calculate the current values (Max, Min, SUM... etc)
    def calculateCurrent(self,currRTT):
        #MIN and MAX
        if currRTT > self.max:
            self.max = currRTT
        if currRTT < self.min:
            self.min = currRTT
        #Get the sum for the average
        self.sum += currRTT
        #Calculate estRTT and devRTT
        self.estRTT = ( 1 - self.a ) * self.estRTT + self.a * currRTT
        self.devRTT =( 1 - self.b ) * self.devRTT + self.b * abs(currRTT - self.estRTT)

    #Given the estRTT and devRTT, calculate the timeout
    def calculateTimeout(self):
        timeout = self.estRTT + 4 * self.devRTT
        return timeout

    #Prints the current time for the reply
    def printCurrent(self,currTime):
        print ("Reply from {0} time = {1}".format(self.ipAddress,currTime))
    
    #Get the aggregate counts/statistics of the Ping run
    def printStats(self):
        #Calculate the average with sum and counts
        avg = self.sum / self.seqCount
        #Calculaate the percentage lost with counts of lost and total
        percentLoss = (self.lost / self.seqCount) * 100
        #Calculate the recieived with the total and counts of lost
        received = self.seqCount - self.lost
        #Calculate Timeout with estRTT and devRTT
        timeout = self.calculateTimeout()
        
        print("Ping statistics for ", self.ipAddress)
        print("\tPackets: Sent = {0}, Received = {1}, Lost = {2} ({3}% loss)".format(self.seqCount, received, self.lost, percentLoss))
        print("Approximate round trip times")
        print("\tMinimum = {0}, Maximum = {1}, Average = {2}".format(self.min, self.max, avg))
        print("\tTimeout = {0}".format(timeout))
        

    def closeSocket(self):
        self.clientSocket.close()
        

#Runs the script    
if __name__ == '__main__':
    portNum = 12000
    ipAdd = '127.0.0.1'
    
    udpClient = UDPPingerClient(portNum, ipAdd)
    totalCount = 0
    while totalCount <10:
        udpClient.sendMessage()
        totalCount += 1
    udpClient.printStats()
    udpClient.closeSocket()
    
