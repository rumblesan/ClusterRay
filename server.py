#!/usr/bin/env python

#Import Modules
import os
import socket
import threading
import Queue
import time

jobQueue = Queue.Queue(0)


class ServerObj():

    def __init__(self):
        self.serverIP       = ''
        self.serverPort     = 5007
    
    def CreateSocket(self):
        openingSocket = True
        while openingSocket:
            try:
                serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error, msg:
                continue
            
            try:
                serverSocket.bind((self.serverIP,self.serverPort))
                serverSocket.listen(5)
            except socket.error, msg:
                serverSocket.close()
                serverSocket = None
                continue
            
            openingSocket = False
        
        return serverSocket


    def CreateJobs(self, numberPerNode, Dimensions):
        pass
        # splits the job up into a number of sub tasks
        # essentially just splits up the povray picture dimensions
        # creates a queue for threads to take jobs from

    def JoinImages(self):
        pass
        # joins the image slices together
 

class ClientThread(threading.Thread):

    def __init__(self, newSocket):
        self.client   = ClientObject(newSocket)
        self.running  = True
        
        threading.Thread.__init__.self
        # create a thread for a particular socket
    
    def run(self):
    
        while self.running:
        
            self.client.GetClientInfo()
            

class ClientObject()

    def __initII(self, newSocket):
        self.clientSocket = newSocket
    
    def GetClientInfo()
        pass
        # receive job instructions from client


class NodeThread(threading.Thread):

    def __init__(self, newSocket):
        self.node    = NodeObject(newSocket)
        self.running = True
        
        threading.Thread.__init__.self
        # create a thread for a particular socket
    
    def run(self):
        
        while self.running:
        
            self.node.GetJob()
            self.node.RunJob()


class NodeObject()

    def __init__(self, newSocket):
        self.nodeSocket = newSocket
        self.jobParams  = None

    def GetJob(self):
        queueing = True
        while queueing:
            jobInfo = jobQueue.Get()
            if jobInfo != None:
                self.jobParams = jobInfo
                queueing = False
            else:
                time.sleep(10)
        
        # try to get a job from the queue
        # sleep for 10 seconds if nothing available

    def RunJob(self):
        pass
        # get a job from the queue and send it to the node

    def RetrieveImage(self):
        pass
        # retrieve an image from a node


if __name__ == '__main__':

    ClusterServer = ServerObj()
    
    global ClusterServer
    global serverSocket
    
    serverRunning = True
    
    while true:
    
        serverSocket = ClusterServer.CreateSocket()
        
        while serverRunning:

            newSocket = serverSocket.accept()
            
            socketType = newSocket.recv(1024)
            
            if socketType == 'node':
                NodeThread(newSocket).start()
            else if socketType == 'client':
                ClientThread(newSocket).start()

