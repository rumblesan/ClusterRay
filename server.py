#!/usr/bin/env python

#Import Modules
import os
import socket
import threading
import Queue
import time
import ftpserver
import re

jobQueue = Queue.Queue(0)
taskQueue = Queue.Queue(0)



class ServerObj():

    def __init__(self):
        self.serverIP       = ''
        self.serverPort     = 5007
        self.serverSocket   = None
    
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
        
        self.serverSocket = serverSocket
 



class FtpThread(threading.Thread):

    def run(self):

        authorizer = ftpserver.DummyAuthorizer()

        fileFolder = os.path.join(os.getcwd(), 'files')
        authorizer.add_user('node', 'cluster', fileFolder, perm='elradfmw')

        ftp_handler = ftpserver.FTPHandler
        ftp_handler.authorizer = authorizer

        ftp_handler.banner = 'Nebula Cluster FTP Server'

        address = ('', 21)
        ftpd = ftpserver.FTPServer(address, ftp_handler)

        ftpd.max_cons = 256
        ftpd.max_cons_per_ip = 5

        ftpd.serve_forever()
        



class ClientThread(threading.Thread):

    def __init__(self, newSocket):
        self.client   = ClientObject(newSocket)
        self.running  = True
        
        threading.Thread.__init__.self
        # create a thread for a particular socket
    
    def run(self):
        while self.running:
            self.client.GetClientInfo()
            

class ClientObject():

    def __init__(self, newSocket):
        self.clientSocket = newSocket
    
    def GetClientInfo():
        fileName = self.clientSocket.recv(1024)
        tarFileName = fileName + '.tar.gz'
        ftpFile = os.path.join(os.getcwd(), 'files', tarFileName)
        if os.path.isfile(ftpFile):
            taskQueue.put(fileName)
            



class TaskThread(threading.Thread):

    def __init__(self, newSocket):
        self.node    = TaskObject()
        self.running = True
        
        threading.Thread.__init__.self

    def run(self):
        
        while self.running:
        
            self.node.GetTask()
            self.node.ReadParams()
            self.CreateJobs()
            jobQueue.join()
            self.JoinImages()
            

class TaskObject():

    def __init__(self, newSocket):
        self.nodeSocket    = newSocket
        self.jobParams     = None
        self.taskFile      = None
        self.taskParams    = None
        self.jobSplitNum   = 8

    def GetTask(self):
        queueing = True
        while queueing:
            taskInfo = taskQueue.Get(True)
            if taskInfo != None:
                self.taskFile = taskInfo
                queueing = False
            else:
                time.sleep(10)

    def ReadParams(self):
        self.tarName = self.taskFile + '.tar.gz'
        tarFile = tarfile.open(self.tarName, mode = 'w:gz')
        tarFile.extractall('temp')
        tarFile.close()
        paramFile = fileFolder = os.path.join(os.getcwd(), 'temp', self.taskFile, 'params.cfg')
        self.taskParams = paramFile.read()

    def CreateJobs(self):
        dif = 1.0 / self.jobSplitNum
        for job in range(self.jobSplitNum):
            colStart = "+SC" + str(job * dif)
            colEnd   = "+EC" + str((job + 1) * dif)
            jobInfo = self.taskParams + " " + colStart + " " + colEnd
            jobQueue.put(jobInfo)

    def JoinImage(self):
        pass
        # Join image files together that have been uploaded to the ftp


class NodeThread(threading.Thread):

    def __init__(self, newSocket):
        self.node    = NodeObject(newSocket)
        self.running = True
        
        threading.Thread.__init__.self
        # create a thread for a particular socket
    
    def run(self):
        
        while self.running:
        
            self.node.GetJob()
            self.node.CreateJobs()


class NodeObject():

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



if __name__ == '__main__':
    
    global ClusterServer
    
    ClusterServer = ServerObj()
    serverRunning = True
    
    FtpThread().start()
    
    while True:
    
        ClusterServer.CreateSocket()
        
        while serverRunning:

            newSocket = ClusterServer.serverSocket.accept()
            
            socketType = newSocket.recv(1024)
            
            if socketType == 'node':
                NodeThread(newSocket).start()
            elif socketType == 'client':
                ClientThread(newSocket).start()

