#!/usr/bin/env python

#Import Modules
import os

class serverObj ():

    def __init__(self):
        self.NodeIPs = 0
        # load config file, create array of node IPs
    
    def CheckNodes(self):
        pass
        # run through array of IPs, check connections and nodes are ok
    
    def SendFile(self, filename):
        pass
        # send a file to each of the nodes
    
    def SplitJob(self, numberPerNode, Dimensions):
        pass
        # splits the job up into a number of sub tasks
        # essentially just splits up the povray picture dimensions
    
    def SendTask(self):
        pass
        # sends a subtask to a node
    
    def RetrieveImage(self):
        pass
        # retrieves an image from a node
    
    
    
