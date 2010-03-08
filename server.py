#!/usr/bin/env python

#Import Modules
import os
import socket
import threading
import Queue
import time
import shutil
import ftpserver
import tarfile
import glob
from PIL import Image

jobQueue = Queue.Queue(0)
taskQueue = Queue.Queue(0)

class ServerObj():

    def __init__(self):
        self.serverIP       = ''
        self.serverPort     = 5007
        self.serverSocket   = None
    
    def CreateSocket(self):
        openingSocket = True
        while openingSocket:
            try:
                serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error, msg:
                continue
            
            try:
                serverSocket.bind((self.serverIP,self.serverPort))
                serverSocket.listen(5)
            except socket.error, msg:
                serverSocket.close()
                serverSocket = None
                continue
            
            openingSocket = False
        
        self.serverSocket = serverSocket
 



class FtpThread(threading.Thread):

    def run(self):

        authorizer = ftpserver.DummyAuthorizer()

        ftpFolder = os.path.join(os.getcwd(), 'files')
        if not os.path.exists(ftpFolder):
            os.mkdir(ftpFolder)
        
        authorizer.add_user('node', 'cluster', ftpFolder, perm='elradfmw')
        authorizer.add_user('client', 'cluster', ftpFolder, perm='elradfmw')

        ftp_handler = ftpserver.FTPHandler
        ftp_handler.authorizer = authorizer

        ftp_handler.banner = 'Nebula Cluster FTP Server'

        address = ('', 21)
        ftpd = ftpserver.FTPServer(address, ftp_handler)

        ftpd.max_cons = 256
        ftpd.max_cons_per_ip = 5

        ftpd.serve_forever()
        



class ClientThread(threading.Thread):

    def __init__(self, newSocket):
        self.client   = ClientObject(newSocket)
        self.running  = True
        threading.Thread.__init__(self)
    
    def run(self):
        self.client.Handshake()
        while self.running:
            self.client.GetClientInfo()
            

class ClientObject():

    def __init__(self, newSocket):
        self.clientSocket = newSocket

    def Handshake(self):
        self.clientSocket.send('connected')

    def GetClientInfo(self):
        fileName = self.clientSocket.recv(1024)
        print fileName
        print 'should have the filename here'
        tarFileName = fileName + '.tar.gz'
        ftpFile = os.path.join(os.getcwd(), 'files', tarFileName)
        if os.path.isfile(ftpFile):
            print 'Client sent file ', fileName
            taskQueue.put(fileName)
            print 'task put in queue'
        else:
            pass
            #print 'No file can be found for ', fileName




class PicJobGen():

    def __init__(self, InputFile, OutputFile, TaskFile, JobNumber, Height, Width, Other):
        self.taskFile      = TaskFile

        self.tempImagesDir = os.path.join(os.getcwd(), 'files', self.taskFile + 'images')
        if not os.path.exists(self.tempImagesDir):
            os.mkdir(self.tempImagesDir)
        
        self.jobNumber     = JobNumber
        self.inputFile     = InputFile
        self.outputFile    = OutputFile
        self.imageHeight   = Height
        self.imageWidth    = Width
        self.otherParams   = Other
    
    def CreateJobs(self):
        dif = 1.0 / self.jobNumber
        print 'function to create jobs'
        for job in range(self.jobNumber):
        
            colStart = str(job * dif)
            colEnd   = str((job + 1) * dif)
            outputFileName = self.outputFile + '_' + str((job) * dif) + '.png'
            
            paramsList = []
            paramsList.append('+I'  + self.inputFile)
            paramsList.append('+O'  + outputFileName)
            paramsList.append('+SC' + colStart)
            paramsList.append('+EC' + colEnd)
            paramsList.append('+H'  + str(self.imageHeight))
            paramsList.append('+W'  + str(self.imageWidth))
            paramsList.append(self.otherParams)
            
            jobInfo = self.taskFile + '::' + outputFileName + '::' + ' '.join(paramsList)
            print jobInfo
            jobQueue.put(jobInfo)
    
    def TaskFinish(self):
        mainDir = os.getcwd()
        os.chdir(self.tempImagesDir)
        widthDiff = self.imageWidth / self.jobNumber
        blankCanvas = Image.new('RGB',(self.imageWidth,self.imageHeight))
        
        for inFile in glob.glob(self.outputFile + '_*.png'):
            file, ext = os.path.splitext(inFile)
            print 'slice join name',file
            taskName,fileNumber = file.split('_')
            section = Image.open(inFile)
            xval = int(self.imageWidth * float(fileNumber))
            slicepos = (xval,0,xval + widthDiff,self.imageHeight)
            print 'slice pos',slicepos
            imageSlice = section.crop(slicepos)
            blankCanvas.paste(imageSlice,slicepos)
        blankCanvas.save(self.outputFile + '.png','PNG')
        os.chdir(mainDir)
        # Join image files together that have been uploaded to the ftp



    def TaskCleanUp(self):
        tempDir = os.path.join(os.getcwd(), 'temp', self.taskFile)
        shutil.rmtree(tempDir)
        # Cleans up temp files and then does something with the picture
        # emails, twitters, posts to flickr etc etc
        

class MovJobGen():

    def __init__(self, InputFile, OutputFile, TaskFile, JobNumber, Height, Width, Other):
        self.taskFile      = TaskFile

        self.tempImagesDir = os.path.join(os.getcwd(), 'files', self.taskFile + 'images')
        if not os.path.exists(self.tempImagesDir):
            os.mkdir(self.tempImagesDir)
        
        self.jobNumber     = JobNumber
        self.inputFile     = InputFile
        self.outputFile    = OutputFile
        self.imageHeight   = Height
        self.imageWidth    = Width
        self.otherParams   = Other
    
    def CreateJobs(self):
        dif = 1.0 / self.jobNumber
        print 'function to create jobs'
        for job in range(self.jobNumber):
        
            colStart = str(job * dif)
            colEnd   = str((job + 1) * dif)
            outputFileName = self.outputFile + '_' + str((job) * dif)
            
            paramsList = []
            paramsList.append('+I'  + self.inputFile)
            paramsList.append('+O'  + outputFileName)
            paramsList.append('+SC' + colStart)
            paramsList.append('+EC' + colEnd)
            paramsList.append('+H'  + str(self.imageHeight))
            paramsList.append('+W'  + str(self.imageWidth))
            paramsList.append(self.otherParams)
            
            jobInfo = self.taskFile + '::' + outputFileName + '::' + ' '.join(paramsList)
            print jobInfo
            jobQueue.put(jobInfo)
    
    def TaskFinish(self):
        mainDir = os.getcwd()
        os.chdir(self.tempImagesDir)
        widthDiff = self.imageWidth / self.jobNumber
        blankCanvas = Image.new('RGB',(self.imageWidth,self.imageHeight))
        
        for inFile in glob.glob(self.outputFile + '_*.png'):
            file, ext = os.path.splitext(inFile)
            print 'slice join name',file
            taskName,fileNumber = file.split('_')
            section = Image.open(inFile)
            xval = int(self.imageWidth * float(fileNumber))
            slicepos = (xval,0,xval + widthDiff,self.imageHeight)
            print 'slice pos',slicepos
            imageSlice = section.crop(slicepos)
            blankCanvas.paste(imageSlice,slicepos)
        blankCanvas.save(self.outputFile + '.png','PNG')
        os.chdir(mainDir)
        # Join image files together that have been uploaded to the ftp



    def TaskCleanUp(self):
        tempDir = os.path.join(os.getcwd(), 'temp', self.taskFile)
        shutil.rmtree(tempDir)
        # Cleans up temp files and then does something with the picture
        # emails, twitters, posts to flickr etc etc


class TaskThread(threading.Thread):

    def __init__(self):
        self.Task    = TaskObject()
        self.running = True
        
        threading.Thread.__init__(self)

    def run(self):
        
        while self.running:
            print 'Task Thread: waiting for task'
            self.Task.GetTask()
            print 'Task Thread: got task ', self.Task.taskFile
            self.Task.ReadParams()
            print 'Task Thread: creating jobs'
            self.Task.jobCreator.CreateJobs()
            print 'Tast Thread: waiting for job queue to be empty'
            jobQueue.join()
            self.Task.jobCreator.TaskFinish()
            self.Task.jobCreator.TaskCleanUp()
            

class TaskObject():

    def __init__(self):
        self.taskFile      = ''
        self.tempImagesDir = ''
        
        self.jobNumber     = ''
        self.inputFile     = ''
        self.outputFile    = ''
        self.renderType    = ''
        self.imageHeight   = ''
        self.imageWidth    = ''
        self.otherParams   = ''
        
        self.jobCreator    = None

    def GetTask(self):
        queueing = True
        while queueing:
            taskInfo = taskQueue.get()
            print 'task queue gots'
            if taskInfo != None:
                self.taskFile = taskInfo
                queueing = False
            else:
                time.sleep(10)

    def ReadParams(self):
        self.tarName = os.path.join(os.getcwd(), 'files', self.taskFile + '.tar.gz')
        tarFile = tarfile.open(self.tarName, mode = 'r:gz')
        tarFile.extractall('temp')
        tarFile.close()
        
        paramFile = open(os.path.join(os.getcwd(), 'temp', self.taskFile, 'params.cfg'))
        for line in paramFile:
            line = line.rstrip()
            line,params = line.split(':')
            if line == 'inputFile':
                self.inputFile   = params
            elif line == 'outputFile':
                self.outputFile   = params
            elif line == 'jobNumber':
                self.jobNumber   = int(params)
            elif line == 'renderType':
                self.renderType   = params
            elif line == 'imageHeight':
                self.imageHeight = int(params)
            elif line == 'imageWidth':
                self.imageWidth = int(params)
            elif line == 'otherParams':
                self.otherParams = params

        paramFile.close()

        if self.renderType == 'picture':
            self.jobCreator = PicJobGen(self.inputFile, self.outputFile, self.taskFile, self.jobNumber, self.imageHeight, self.imageWidth, self.otherParams)
        elif self.renderType == 'picture':
            self.jobCreator = MovJobGen()
        print 'Task Thread: read param'



class NodeThread(threading.Thread):

    def __init__(self, newSocket):
        self.node    = NodeObject(newSocket)
        threading.Thread.__init__(self)
        # create a thread for a particular socket

    def run(self):
        self.node.running = self.node.Handshake()
        while self.node.running:
            self.node.GetJob()
            self.node.RunJob()


class NodeObject():

    def __init__(self, newSocket):
        self.nodeSocket = newSocket
        self.jobParams  = None
        self.running    = False

    def Handshake(self):
        connectCheck = self.nodeSocket.send('connected')
        if connectCheck == 0:
            return False
        else:
            return True

    def GetJob(self):
        queueing = True
        while queueing:
            print 'node thread looking for jobs'
            jobInfo = jobQueue.get()
            print 'node thread looking for jobs'
            self.jobParams = jobInfo
            queueing = False

    def RunJob(self):
        print 'node thread running job perhaps'
        self.nodeSocket.send('jobs available')
        nodeInfo = self.nodeSocket.recv(1024)
        if nodeInfo == '':
            self.running = False
            return False
        if nodeInfo == 'info':
            self.nodeSocket.send(self.jobParams)
            jobRunning = True
            while jobRunning:
                jobStatus = self.nodeSocket.recv(1024)
                if jobStatus == 'Completed':
                    jobQueue.task_done()
                    jobRunning = False


if __name__ == '__main__':
    
    global ClusterServer
    
    ClusterServer = ServerObj()
    serverRunning = True
    
    tempFolder = os.path.join(os.getcwd(), 'temp')
    if not os.path.exists(tempFolder):
        os.mkdir(tempFolder)
    
    FtpThread().start()
    TaskThread().start()
    
    while True:
    
        print 'Serving Network requests on port ', ClusterServer.serverPort
        ClusterServer.CreateSocket()
        
        while serverRunning:

            newSocket, address = ClusterServer.serverSocket.accept()
            newSocket.setblocking(1)
            socketType = newSocket.recv(1024)
            
            if socketType == 'node':
                print 'Node connection from ',address
                NodeThread(newSocket).start()
            elif socketType == 'client':
                print 'Client connection from ',address
                ClientThread(newSocket).start()

