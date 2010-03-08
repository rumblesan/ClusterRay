#!/usr/bin/env python

#Import Modules
import os
import socket
import time
import tarfile
import ftplib
import shutil

class NodeObj ():

    def __init__(self):
        # details of main server
        # will eventually be in cfg file
        # possibly host name based
        self.serverIP        = '192.168.2.14'
        self.serverPort      = 5007
        self.serverSocket    = None

        self.ftpServer       = self.serverIP 
        self.ftpUser         = 'node'
        self.ftpPass         = 'cluster'

        self.jobParams       = None
        self.jobFile         = None
        self.outputFile      = None

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
                self.jobFile = jobInfo[0]
                self.outputFile = jobInfo[1]
                self.jobParams = jobInfo[2]
                checking = False
            else:
                time.sleep(10)
        return 1

    def FtpDownload(self):
        # download tar.gz file from the ftp server
        ftpSocket = ftplib.FTP(self.ftpServer,self.ftpUser,self.ftpPass)
        tarName = self.jobFile + '.tar.gz'
        print 'downloading from ftp', tarName
        tarFile = open(tarName,"wb")
        ftpSocket.retrbinary("RETR " + tarName, tarFile.write)
        tarFile.close()
        ftpSocket.quit()
        
    def UntarFile(self):
        print 'untarring file'
        tarName = self.jobFile + '.tar.gz'
        tarFile = tarfile.open(tarName, mode = 'r:gz')
        tarFile.extractall('nodetemp')
        tarFile.close()
        os.remove(tarName)
        
    def RunJob(self):
        mainDir = os.getcwd()
        jobDir = os.path.join(os.getcwd(), 'nodetemp', self.jobFile)
        os.chdir(jobDir)
        running = 'povray ' + self.jobParams
        print 'running job now'
        print running
        output = os.system(running)
        print output
        os.chdir(mainDir)
        # run povray from the command line
        # use self.jobParams as the arguments
       
        
    def UploadOutputFile(self):
        # upload tar.gz file to the ftp server
        # probablly want error checking
        print 
        ftpSocket = ftplib.FTP(self.ftpServer,self.ftpUser,self.ftpPass)
        ftpDirFolder = self.jobFile + 'images'
        ftpSocket.cwd(ftpDirFolder)
        uploadFile = os.path.join(os.getcwd(), 'nodetemp', self.jobFile, self.outputFile)
        fileHandle = open(uploadFile,'rb')
        ftpSocket.storbinary('STOR ' + self.outputFile, fileHandle)
        fileHandle.close()
        ftpSocket.quit()
        
    def CompletedTask(self):
        tempFiles = os.path.join(os.getcwd(), 'nodetemp', self.jobFile)
        shutil.rmtree(tempFiles)
        self.serverSocket.send('Completed')
        # send job completion message back
        # format output of job program
        # send job information back


if __name__ == '__main__':

    clusterNode = NodeObj()
    
    tempFolder = os.path.join(os.getcwd(), 'nodetemp')
    if not os.path.exists(tempFolder):
        os.mkdir(tempFolder)
    
    while True:
        print 'trying to connect to server'
        clusterNode.ServerConnect()
        print 'connected to server'
        clusterNode.Handshake()
        print 'handshake ok'
        
        while clusterNode.connectedServer:
            print 'checking for jobs'
            if clusterNode.CheckForJobs():
                clusterNode.FtpDownload()
                clusterNode.UntarFile()
                clusterNode.RunJob()
                clusterNode.UploadOutputFile()
                clusterNode.CompletedTask()
                
