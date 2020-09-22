import threading
import sys
import socket

global clientName, received

#listens to socket and addr
def listenToClientMessage(cSocket, addr):

    #recieves from message from port
    message = cSocket.recv(1024)
    clName = message.split(':')[0]
    clientName[clName] = cSocket
    received.append(message)
    print("Client " + message)
    # check if both clients have sent messages
    #if so sends to all clients
    if (len(received) == 2):
        sendToAllClients()

#listens to new connections
def listenToNewConnections(s):
    count = 0
    while count != 2:
        c, addr = s.accept()
    worker = threading.Thread(target=listenToClientMessage, args=[c, addr])
    worker.start()
    count += 1

#get server sockets, listens and returns value
def getServerSocket():
    #functino to count the number of arguements
    port = int(sys.argv[1])
    ip = '127.0.0.1'
    s = socket.socket()
    #combines ip and port to listen
    s.bind((ip, port))
    #listening
    s.listen(5)
    return s

#sends message of acknowledgment to clients
def sendToAllClients():
    for (name, c) in clientName.items():
        c.send("%s received before %s" % (received[0], received[1]))
        c.close()
print("Sent acknowledgment to both X and Y")

#main to set up program
def main():
    global clientName, received
    #defines dict
    clientName = {}
    received = []
    # Initialize server socket to listen to connections
    s = getServerSocket()
    # start listening to new connections
    listenToNewConnections(s)


main()

