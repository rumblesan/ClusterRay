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

        # command line params and file list
        self.jobParams       = None
        self.jobFiles        = None

        # node states
        self.connectedServer = False
        self.taskRunning     = False

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
        
        return 1

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
        while checking
            self.wakeSocket.send('work')
            jobStatus = self.wakeSocket.recv(1024)
            if jobStatus == 'available':
                waiting = False
            else:
                time.sleep(2)

    def GetJobInfo(self):
        pass
        #get the job files and params

    def RunJob(self):
        # run the job process
        pass

    def CleanUp(self):
        # deletes all local files
        # closes job listening socket
        pass


if __name__ == '__main__':

    clusterNode = NodeObj()

    while true:
        clusterNode.ServerConnect()
        clusterNode.Handshake()
        
        while clusterNode.connectedServer:
            clusterNode.CheckForJobs()
            
            while clusterNode.taskRunning:
                clusterNode.RunJob()
            

