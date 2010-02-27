#!/usr/bin/env python

#Import Modules
import os
import socket
import time
import tarfile

class ClientObj ():

    def __init__(self):
        # details of main server
        # will eventually be in cfg file
        # possibly host name based
        self.serverIP        = '192.168.0.50'
        self.serverPort      = 6007
        
        self.ftpServer       = self.serverIP
        self.ftpUser         = 'client'
        self.ftpPass         = 'client'

        self.folderName      = ''
        self.tarName         = ''
        
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
        # tell it that this is a client
        waiting = True
        while waiting:
            self.serverSocket.send('client')
            serverStatus = self.serverSocket.recv(1024)
            if serverStatus == 'connected':
                waiting = False
            else:
                time.sleep(2)
                
        return serverStatus

    def GetFolderName(self):
        name = raw_input("type name of folder")
        if os.path.isdir(name):
            return True
        else:
            print "this is not a folder"
            return False

    def SendTask(self):
        # sends a task to the server
        # uploads files to a new folder on the ftp server
        # send the folder name tothe server
        pass

    def TarFolder(self):
    
        self.tarName = self.folderName + '.tar.gz'
        try:
            tarFile = tarfile.open(self.tarName, mode = 'w:gz')
            tarFile.add(self.folderName)
            tarFile.close()
            return True
        except:
            return None

    def FtpUpload(self):
        s = ftplib.FTP(self.ftpServer,self.ftpUser,self.ftpPass)

        f = open(self.tarName,'rb')
        s.storbinary('STOR ' + self.tarName, f)

        f.close()
        s.quit()





if __name__ == '__main__':

    Client = ClientObj()
    job    = JobObj()
    
    while true:
        Client.ServerConnect()
        Client.Handshake()
        
        while Client.connectedServer:
            if Client.GetFolderName:
                Client.TarFolder()
                Client.FtpUpload()
                Client.SendTask()
            else:
                time.sleep(3)
            # wait for user to define jobs
            # send jobs to server
