#TCPCapitalizationServer.py
from socket import *
from threading import Thread
from threading import Semaphore
import time

#GLOBAL VARIABLES

#holds the current Client
currClient = []


#Semaphore lock
sema_lock = Semaphore()

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
   global bothMsg
   while True:
      msg = clientSocket.recv(1024).decode()
      print("Got Message {}".format(msg))
      #exit program if message is bye
      if msg == 'bye':
         break
      else:
        currClient.append(msg)
        printServer("List Size " + str(len(currClient)))
        twoItemCheck = False
        while not twoItemCheck:
            printServer("Checking if length is two")
            if len(currClient) == 2:
                bothMsg = True
                getMsg()
                clientSocket.send(newMessage.encode())
                printServer("New Message: " + newMessage)
                twoItemCheck = True
                break
            elif bothMsg:
                time.sleep(2)
                clientSocket.send(newMessage.encode())
                twoItemCheck = True
                break
            time.sleep(2)
            
      break

#Lock for Semaphore printing
def printServer(toPrint):
   sema_lock.acquire()
   print(toPrint)
   sema_lock.release()
   time.sleep(0.25)

def sendMessage(socket,msg):
   socket.send(msg)
   socket.close()

#MAIN
if __name__ == '__main__':
   serverPort = 12000
   serverSocket = socket(AF_INET,SOCK_STREAM)
   serverSocket.bind(('',serverPort))
   serverSocket.listen(5)
   print("Server Currently Waiting for Message...")
   while True:
      print('new message received')
      connectionSocket, addr = serverSocket.accept()
      print("connected to {0}".format(addr))
      Thread(target=run,args = (connectionSocket, addr)).start()
      time.sleep(.25)
   connectionSocket.close()
