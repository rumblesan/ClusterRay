#!/usr/bin/env python

#Import Modules
import os
import socket

class NodeObj ():

    def __init__(self):
        self.serverIP        = "192.168.0.50"
        self.serverPort      = 6007
        self.jobPort         = None

        self.wakeSocket      = None
        self.jobSocket       = None

        self.jobParams       = None
        self.jobFile         = None

        self.findingServer   = True
        self.connectingJob   = False
        self.connectedServer = False
        self.taskRunning     = False

    def GetJobfile(self):
        pass
        # send a request for the jobFile

    def RunProcess(self):
        pass
        # run the job process

    def SendStatus(self):
        pass
        # send the status of the job to the server
        # called when the job finishes

    def CleanUp(self):
        pass
        # deletes all local files
        # closes job listening socket


if __name__ == '__main__':

    clusterNode = NodeObj()

    while clusterNode.findingServer:
        try:
            clusterNode.wakeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            continue

        try:
            clusterNode.wakeSocket.connect((clusterNode.serverIP,clusterNode.serverPort))
        except socket.error, msg:
            clusterNode.wakeSocket.close()
            clusterNode.wakeSocket = None
            continue

        clusterNode.findingServer = False
        clusterNode.connectingJob = True
        clusterNode.jobPort = clusterNode.wakeSocket.recv(1024)


    while clusterNode.connectingJob:

        try:
            clusterNode.jobSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            continue

        try:
            clusterNode.jobSocket .connect((clusterNode.serverIP,clusterNode.jobPort))
        except socket.error, msg:
            clusterNode.jobSocket .close()
            clusterNode.jobSocket = None
            continue

        clusterNode.connectingJob = False
        clusterNode.connectedServer = True

    while self.connectedServer:
        
        

