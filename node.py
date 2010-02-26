#!/usr/bin/env python

#Import Modules
import os
import socket
import time

class NodeObj ():

    def __init__(self):
        # details of main server
        # will eventually be in cfg file
        # possibly host name based
        self.serverIP        = "192.168.0.50"
        self.serverPort      = 6007

        # network socket connected to server
        self.serverSocket    = None

        # node states
        self.connectedServer = False

    def ServerConnect(self):
        # keep trying to connect to server
        while !self.connectedServer:
            try:
                self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error, msg:
                time.sleep(2)
                continue

            try:
                self.serverSocket.connect((self.serverIP,self.serverPort))
            except socket.error, msg:
                self.serverSocket.close()
                self.serverSocket = None
                time.sleep(2)
                continue

            self.serverSocket.setblocking(1)
            self.connectedServer = True

    def Handshake(self):
        # check in with the server
        # tell it that this is a node
        waiting = True
        while waiting:
            self.wakeSocket.send('node')
            serverStatus = self.wakeSocket.recv(1024)
            if serverStatus == 'connected':
                waiting = False
            else:
                time.sleep(2)
                
        return serverStatus
        
    def CheckForJobs(self):
        # waits untill it gets a job
        checking = True
        while checking:
            self.wakeSocket.send('work')
            jobStatus = self.wakeSocket.recv(1024)
            if jobStatus == 'available':
                # get files transfered over
                # get job params transfered over
                job.jobParams   = None
                job.jobFileList = None
                checking        = False
            else:
                time.sleep(10)
        return 1


class JobObj():

    def __init__(self):
        self.jobParams    = ''
        self.jobFileList  = ''
    
    def RunJob(self):
        # run the job process
        pass

    def ReturnInfo(self):
        # send job completion message back
        # format output of job program
        #send job information back


if __name__ == '__main__':

    clusterNode = NodeObj()
    job         = JobObj()
    
    while true:
        clusterNode.ServerConnect()
        clusterNode.Handshake()
        
        while clusterNode.connectedServer:
            if clusterNode.CheckForJobs():
                job.RunJob
