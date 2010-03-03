#!/usr/bin/env python

#Import Modules
import os
import socket
import time
import tarfile
import ftplib

class ClientObj ():

    def __init__(self):
        # details of main server
        # will eventually be in cfg file
        # possibly host name based
        self.serverIP        = '192.168.2.4'
        self.serverPort      = 5007
        
        self.ftpServer       = self.serverIP
        self.ftpUser         = 'client'
        self.ftpPass         = 'cluster'

        self.folderName      = ''
        self.tarName         = ''
        
        # network socket connected to server
        self.serverSocket    = None

        # node states
        self.connectedServer = False

    def ServerConnect(self):
        # keep trying to connect to server
        while self.connectedServer == False:
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
        # Get foldername to send to server from user
        # check that folder exists
        # this is a pretty rubbish way of sending tasks
        # need to come up with a better way
        print 'Enter name of folder'
        name = raw_input('>>>   ')
        if os.path.isdir(name):
            print 'Folder ok, uploading now'
            self.folderName = name
            return True
        else:
            print 'This is not a folder'
            return False

    def TarFolder(self):
        # put chosen folder into a gzipped tar file
        self.tarName = self.folderName + '.tar.gz'
        try:
            tarFile = tarfile.open(self.tarName, mode = 'w:gz')
            tarFile.add(self.folderName)
            tarFile.close()
            return True
        except:
            return None

    def FtpUpload(self):
        # upload tar.gz file to the ftp server
        # probablly want error checking
        ftpSocket = ftplib.FTP(self.ftpServer,self.ftpUser,self.ftpPass)
        fileHandle = open(self.tarName,'rb')
        ftpSocket.storbinary('STOR ' + self.tarName, fileHandle)
        fileHandle.close()
        ftpSocket.quit()
        os.remove(self.tarName)

    def SendTask(self):
        # send name of uploaded file to server
        self.serverSocket.send(self.folderName)




if __name__ == '__main__':

    Client = ClientObj()
    
    while True:
        print 'Client is trying to connect to server'
        Client.ServerConnect()
        print 'Client is connected'
        print 'Client is handshaking'
        Client.Handshake()
        print 'Handshake OK'
        
        while Client.connectedServer:
            if Client.GetFolderName():
                print 'Creating Tar file'
                Client.TarFolder()
                print 'Uploading to FTP server'
                Client.FtpUpload()
                print 'Sending server task name'
                Client.SendTask()
                # probablly want notification of when task is done
                # possibly another thread so more jobs can be sent as well
            else:
                time.sleep(3)

