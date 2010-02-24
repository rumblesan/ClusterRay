#!/usr/bin/env python

#Import Modules
import os
import socket
import threading
import Queue

class serverObj ():

    def __init__(self, configFile):
        self.nodeIPs = 0
        self.nodeThreads = 0
        self.jobQueue = 0
        self.taskRunning = False
        # load config file, create array of node IPs
    
    def CheckNodes(self):
        pass
        # run through array of IPs, check connections and nodes are ok
    
    def CreateThreads(self):
        self.taskRunning = True
        # creates a thread for each IP in the node list
        # sets the task running as it creates each node
    
    def SplitJob(self, numberPerNode, Dimensions):
        pass
        # splits the job up into a number of sub tasks
        # essentially just splits up the povray picture dimensions
        # creates a queue for threads to take jobs from

    def JoinImages(self):
        pass
        # joins the image slices together

class NodeThread( threading.Thread ):

    def __init__(self, IPAdr, Port):
        self.NodeIPs = 0
        self.socket
        self.working = 0
        # load config file, create array of node IPs
    
    def SendFile(self, filename):
        pass
        # send a file to each of the nodes

    def RetrieveImage(self):
        pass
        # retrieves an image from a node
    
    def CleanupNode(self, nodeNumber):
        pass
        # deletes any files off nodes


if __name__ == '__main__':

    nodeTasks = 2
    width     = 1024
    height    = 768

    ClusterServer = serverObj (configFile)
    ClusterServer.CheckNodes()
    ClusterServer.SplitJob(nodeTasks, (width, height))
    ClusterServer.CreateThreads()

    while ClusterServer.taskRunning:
        pass


    ClusterServer.JoinImages()
