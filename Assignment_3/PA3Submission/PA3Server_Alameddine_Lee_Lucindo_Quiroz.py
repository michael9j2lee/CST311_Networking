# CST 311
# Programming Assignment 3
# Amir-Andy Alameddine
# Michael Lee
# Ramon Lucindo
# Sergio Quiroz
# PA3Server_Alameddine_Lee_Lucindo_Quiroz.py

from socket import *
from threading import Thread
from threading import Semaphore
import time

#GLOBAL VARIABLES

#holds the current Client
currClient = []


#Semaphore lock
sema_lock = Semaphore()

#Holds the Bool for when both messages are received.
bothMsg = False
newMessage = ''

#Detect the Order of Message depending on client
def getMsg():
   global currClient, newMessage
   client1 = currClient[0]
   client2 = currClient[1]
   newMessage = '{0} received before {1}'.format(client1,client2)
   printServer(newMessage)

#The multithreaded command
def run (clientSocket, address):
   #Holds the global boolean
   global bothMsg
   while True:
      msg = clientSocket.recv(1024).decode()
      print("Got Message {}".format(msg))
      #exit program if message is bye
      if msg == 'bye':
         break
      #if message is not bye
      else:
        #Add to the list that holds the messages
        currClient.append(msg)
        #Prints current list size
        printServer("List Size " + str(len(currClient)))
        twoItemCheck = False
        #Check if there are two items
        while not twoItemCheck:
            #printServer("Checking if length is two")
            #If there are two items already in the list (Kinda of like queue)
            if len(currClient) == 2:
                bothMsg = True
                #Gets message from with the getMsg function
                getMsg()
                #Send the message to the client (whichever one sent it)
                clientSocket.send(newMessage.encode())
                #Prints the new messages that was sent with the semaphore lock
                printServer("New Message: " + newMessage)
                #Sets the twoItem Check to true to exit out of this thread
                twoItemCheck = True
                #Exit Loop for the two Item check
                break
            #If there are two items already in the queue GLOBAL VARIABLE bothMsg
            elif bothMsg:
                #Sleep to wait for the second message
                time.sleep(2)
                #Send message 
                clientSocket.send(newMessage.encode())
                #Looks like there are two items, we set the twoItemCheck to True to exit.
                twoItemCheck = True
                #Exit Loop for the two Item check
                break
            #Time to sleep
            time.sleep(2)
      #we Exit out of the main loop to close the thread
      break

#Lock for Semaphore printing
#Simple lock mechanism to make sure print doesn't get jumbled.
def printServer(toPrint):
   sema_lock.acquire()
   print(toPrint)
   sema_lock.release()
   time.sleep(0.25)

#MAIN
if __name__ == '__main__':
   #Set the server configurations
   serverPort = 12000
   serverSocket = socket(AF_INET,SOCK_STREAM)
   serverSocket.bind(('',serverPort))
   serverSocket.listen(5)
   print("Server Currently Waiting for Message...")
   #while loop when a message is received, we start a new thread
   while True:
      print('new message received')
      connectionSocket, addr = serverSocket.accept()
      print("connected to {0}".format(addr))
      #Start the thread with the run method (See above)
      Thread(target=run,args = (connectionSocket, addr)).start()
      #Sleep just in case
      time.sleep(.25)
   #Close the socket when it is done
   connectionSocket.close()
