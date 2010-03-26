#!/usr/bin/env python

#Import Modules
import os
import sys
import socket
import time
import tarfile
import ftplib
import shutil
import threading
from daemon import Daemon

tempFolder = '/var/tmp/clusterTemp'
logFile    = '/var/log/RenderNode.log'
pidFile    = '/var/run/renderNode.pid'
serverPort = 5007
ftpPort    = 3457
serverIP   = '192.168.2.14'

class NodeObj ():

    def __init__(self):
        # details of main server
        # will eventually be in cfg file
        # possibly host name based
        self.serverIP        = serverIP
        self.serverPort      = serverPort
        self.serverSocket    = None

        self.ftpServer       = self.serverIP
        self.ftpPort         = ftpPort
        self.ftpUser         = 'node'
        self.ftpPass         = 'cluster'

        self.jobParams       = None
        self.jobFile         = None
        self.outputFile      = None

        # node states
        self.connectedServer = False

    def ServerConnect(self):
        LogFile.WriteLine('Node: Trying to connect to server')
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
        LogFile.WriteLine('Node: Connected to server')
        return 1

    def Handshake(self):
        # check in with the server
        # tell it that this is a node
        while True:
            try:
                sendData = self.serverSocket.send('node')
                if sendData == 0:
                    LogFile.WriteLine('Node: Connection to server has died. Will sleep then reconnect')
                    time.sleep(5)
                    self.connectedServer = False
                    return 0
                serverStatus = self.serverSocket.recv(1024)
                if serverStatus == 'connected':
                    LogFile.WriteLine('Node: Hanshake OK')
                    return 1
                else:
                    LogFile.WriteLine('Node: Problems connecting, sleep then try to reconnect')
                    time.sleep(2)
                    return 0
            except socket.error, msg:
                LogFile.WriteLine('Node: Problems connecting, sleep then try to reconnect')
                time.sleep(2)
                return 0

        
    def CheckForJobs(self):
        LogFile.WriteLine('Node: Checking for jobs')
        while True:
            LogFile.WriteLine('Node: Checking for job status')
            jobStatus = self.serverSocket.recv(1024)
            if jobStatus == 'jobs available':
                LogFile.WriteLine('Node: Jobs available')
                sendData = self.serverSocket.send('info')
                if sendData == 0:
                    LogFile.WriteLine('Node: Connection to server has died. Will sleep then reconnect')
                    time.sleep(5)
                    self.connectedServer = False
                    return 0
                jobInfo = self.serverSocket.recv(1024)
                if jobInfo == '':
                    LogFile.WriteLine('Node: Connection to server has died. Will sleep then reconnect')
                    time.sleep(5)
                    self.connectedServer = False
                    return 0
                LogFile.WriteLine('Node: Job informaion received')
                LogFile.WriteLine('Node: ' + jobInfo)
                jobInfo = jobInfo.split('::')
                self.jobFile = jobInfo[0]
                self.outputFile = jobInfo[1]
                self.jobParams = jobInfo[2]
                return 1
            elif jobStatus == '':
                LogFile.WriteLine('Node: Connection to server has died. Will sleep then reconnect')
                time.sleep(5)
                self.connectedServer = False
                return 0
            else:
                LogFile.WriteLine('Node: Sleeping')
                time.sleep(10)
        return 1

    def FtpDownload(self):
        # download tar.gz file from the ftp server
        
        ftpSocket = ftplib.FTP()
        ftpSocket.connect(self.ftpServer,self.ftpPort)
        ftpSocket.login(self.ftpUser,self.ftpPass)
        
        tarName = self.jobFile + '.tar.gz'
        LogFile.WriteLine('Node: Downloading file from FTP')
        LogFile.WriteLine('Node: ' + tarName)
        tarFile = open(tarName,"wb")
        ftpSocket.retrbinary("RETR " + tarName, tarFile.write)
        tarFile.close()
        ftpSocket.quit()
        LogFile.WriteLine('Node: File downloaded OK')
        
    def UntarFile(self):
        LogFile.WriteLine('Node: Untaring file')
        tarName = self.jobFile + '.tar.gz'
        tarFile = tarfile.open(tarName, mode = 'r:gz')
        tarFile.extractall(tempFolder)
        tarFile.close()
        os.remove(tarName)
        
    def RunJob(self):
        mainDir = os.getcwd()
        jobDir = os.path.join(tempFolder, self.jobFile)
        os.chdir(jobDir)
        running = 'povray ' + self.jobParams
        LogFile.WriteLine('Node: Running job now')
        LogFile.WriteLine('Node: ' + running)
        output = os.system(running)
        os.chdir(mainDir)
        LogFile.WriteLine('Node: finished job')
        return output
        # run povray from the command line
        # use self.jobParams as the arguments
       
        
    def UploadOutputFile(self):
        # upload tar.gz file to the ftp server
        # probablly want error checking
        LogFile.WriteLine('Node: Uploading output file to ftp server')
        ftpSocket = ftplib.FTP()
        ftpSocket.connect(self.ftpServer,self.ftpPort)
        ftpSocket.login(self.ftpUser,self.ftpPass)
        ftpDirFolder = self.jobFile + 'images'
        ftpSocket.cwd(ftpDirFolder)
        uploadFile = os.path.join(tempFolder, self.jobFile, self.outputFile)
        fileHandle = open(uploadFile,'rb')
        ftpSocket.storbinary('STOR ' + self.outputFile, fileHandle)
        fileHandle.close()
        ftpSocket.quit()
        
    def CompletedTask(self):
        LogFile.WriteLine('Node: Clearing up temp dirs')
        tempFiles = os.path.join(tempFolder, self.jobFile)
        shutil.rmtree(tempFiles)
        sentOK = self.serverSocket.send('Completed')
        if sentOK == 0:
            LogFile.WriteLine('Node: Connection to server has died. Will sleep then reconnect')
            time.sleep(5)
            self.connectedServer = False
            return 0
        # send job completion message back
        # format output of job program
        # send job information back

    def JobError(self):
        LogFile.WriteLine('Node: Problem running job')
        LogFile.WriteLine('Node: Clearing up temp dirs')
        tempFiles = os.path.join(tempFolder, self.jobFile)
        shutil.rmtree(tempFiles)
        LogFile.WriteLine('Node: Telling server job had errors')
        self.serverSocket.send('Error')
        if sentOK == 0:
            LogFile.WriteLine('Node: Connection to server has died. Will sleep then reconnect')
            time.sleep(5)
            self.connectedServer = False
            return 0
        # send job completion message back
        # format output of job program
        # send job information back

class LoggingObj():
 
    def __init__(self):
        self.logFile = logFile
        self.fileHandle = open(self.logFile, 'a')
        self.logFileLock = threading.Lock()
 
    def WriteLine(self, logLine):
        self.logFileLock.acquire()
        output = self.TimeStamp() + ' ' + str(logLine) + '\n'
        self.fileHandle.write(output)
        self.logFileLock.release()
    
    def TimeStamp(self):
        stamp = time.strftime("%Y%m%d-%H:%M:%S")
        return stamp



class NodeDaemon(Daemon):
    
    def run(self):
        
        LogFile.WriteLine('Checking that all necesarry folders are available')
        
        if not os.path.exists(tempFolder):
            os.mkdir(tempFolder)

        clusterNode = NodeObj()
        
        while True:
            
            if clusterNode.ServerConnect():
                
                if clusterNode.Handshake():
                    
                    while clusterNode.connectedServer:
                        
                        if clusterNode.CheckForJobs():
                            clusterNode.FtpDownload()
                            clusterNode.UntarFile()
                            jobState = clusterNode.RunJob()
                            if not jobState:
                                LogFile.WriteLine('Node: Job run fine')
                                clusterNode.UploadOutputFile()
                                clusterNode.CompletedTask()
                            else:
                                clusterNode.JobError()
                else:
                    LogFile.WriteLine('Node: Could not handshake')
                    time.sleep(2)
            else:
                LogFile.WriteLine('Node: Could not connect to server')
                time.sleep(10)

if __name__ == "__main__":

        global LogFile
        LogFile = LoggingObj()
        
        LogFile.WriteLine('\n\n')
        LogFile.WriteLine('Cluster Node Starting Up')
        LogFile.WriteLine('')
        daemon = NodeDaemon(pidFile)
        
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        LogFile.WriteLine('Starting Daemon')
                        daemon.start()
                elif 'foreground' == sys.argv[1]:
                        LogFile.WriteLine('Running in foreground')
                        daemon.run()
                elif 'stop' == sys.argv[1]:
                        LogFile.WriteLine('Stopping Daemon')
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        LogFile.WriteLine('Restarting Daemon')
                        daemon.restart()
                else:
                        LogFile.WriteLine('Unknown Command')
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart|foreground" % sys.argv[0]
                sys.exit(2)
                


