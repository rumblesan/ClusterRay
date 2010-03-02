#!/usr/bin/env python

#Import Modules
import os
import socket
import time
import tarfile

class NodeObj ():

    def __init__(self):
        # details of main server
        # will eventually be in cfg file
        # possibly host name based
        self.serverIP        = '192.168.2.4'
        self.serverPort      = 5007

        # network socket connected to server
        self.serverSocket    = None

        # node states
        self.connectedServer = False

    def ServerConnect(self):
        # keep trying to connect to server
        while not self.connectedServer:
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
            self.serverSocket.send('node')
            serverStatus = self.serverSocket.recv(1024)
            if serverStatus == 'connected':
                waiting = False
            else:
                time.sleep(2)
                
        return serverStatus
        
    def CheckForJobs(self):
        # waits untill it gets a job
        checking = True
        while checking:
            print 'checking for job status'
            jobStatus = self.serverSocket.recv(1024)
            if jobStatus == 'jobs available':
                print 'jobs available'
                self.serverSocket.send('info')
                jobInfo = self.serverSocket.recv(1024)
                jobInfo = jobInfo.split('::')
                job.jobFile = jobInfo[0]
                job.jobParams = jobInfo[1]
                print job.jobFile
                print job.jobParams
                checking = False
            else:
                time.sleep(10)
        return 1
        
    def CompletedTask(self):
        self.serverSocket.send('Completed')
        # send job completion message back
        # format output of job program
        # send job information back


class JobObj():

    def __init__(self):
        self.jobParams    = ''
        self.jobFile  = ''

    def DownloadFile(self):
        pass
        # download the file from the ftp server
    
    def UntarFile(self):
        tarName = self.jobFile + '.tar.gz'
        tarFile = tarfile.open(tarName, mode = 'w:gz')
        # need to check that the working dir is there
        # if not, create it
        tarFile.extractall('working')
        tarFile.close()

    def RunJob(self):
        pass
        # run povray from the command line
        # use self.jobParams as the arguments

    def UploadOutputFile(self):
        pass
        # need to upload output files to ftp server
        # file params needs to define output file
        # also folder to upload to


if __name__ == '__main__':

    clusterNode = NodeObj()
    job         = JobObj()
    
    while True:
        print 'trying to connect to server'
        clusterNode.ServerConnect()
        print 'connected to server'
        clusterNode.Handshake()
        print 'handshake ok'
        
        while clusterNode.connectedServer:
            print 'checking for jobs'
            if clusterNode.CheckForJobs():
                job.DownloadFile()
                job.UntarFile()
                job.RunJob()
                clusterNode.CompletedTask()
                
