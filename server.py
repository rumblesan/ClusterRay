#!/usr/bin/env python

#Import Modules
import os
import socket
import threading
import Queue

jobQueue = Queue.Queue(0)
lock = thread.allocate_lock()


class ServerObj():

    def __init__(self):
        self.serverIP = None
        self.basePort = 5007
        self.baseSocket = None
        
        self.threadNumber = 0
        self.jobQueue = 0
        
        self.startingUp  = True
        self.taskRunning = False
    
    def CreateSocket(self):
        while self.startingUp:
            try:
                self.baseSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error, msg:
                continue
            
            try:
                self.baseSocket.bind((self.serverIP,self.basePort))
                self.baseSocket.listen(5)
            except socket.error, msg:
                self.baseSocket.close()
                self.baseSocket = None
                continue
                
            self.baseSocket.settimeout(5)
            self.startingUp = False
            self.taskRunning = True

    def CreateJobs(self, numberPerNode, Dimensions):
        pass
        # splits the job up into a number of sub tasks
        # essentially just splits up the povray picture dimensions
        # creates a queue for threads to take jobs from

    def JoinImages(self):
        pass
        # joins the image slices together
 

class NodeThread(threading.Thread):

    def __init__(self, nodeSocket):
        self.node = NodeObject(nodeSocket)
        self.running = True
        
        threading.Thread.__init__.self
        # create a thread for a particular socket
    
    def run(self):
    
        lock.acquire()
        ClusterServer.threadnumber += 1
        lock.release()
        
        self.node.sendFiles()
        self.node.HandShake()
        while self.running:
            self.node.RunTask()
            self.node.WaitForTask()
            self.node.RetrieveImage()
        
        self.node.CleanupNode()
        lock.acquire()
        ClusterServer.threadnumber -= 1
        if ClusterServer.threadnumber == 0:
            ClusterServer.taskRunning = False
        lock.release()

class NodeObject()

    def __init__(self, nodeSocket):
        self.socket = nodeSocket

    def SendFiles(self, filename):
        pass
        # send a file to the node
    
    def RunTask(self):
        pass
        # get a job from the queue and send it to the node

    def HandShake(self):
        pass
        # check that the node is ready to go

    def WaitForTask(self):
        pass
        # wait for the task to be completed

    def RetrieveImage(self):
        pass
        # retrieve an image from a node
    
    def CleanupNode(self):
        pass
        # deletes any files off nodes


if __name__ == '__main__':

    nodeTasks = 2
    width     = 1024
    height    = 768

    ClusterServer = ServerObj()
    global ClusterServer
    
    ClusterServer.CreateJobs(nodeTasks, (width, height))
    
    ClusterServer.CreateSocket()

    while ClusterServer.taskRunning:
        try:
            socket = ClusterServer.baseSocket.accept()
            socket.settimeout(None)
            NodeThread(socket).start()
        except socket.timeout
            pass



    ClusterServer.JoinImages()
