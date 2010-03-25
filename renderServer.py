#!/usr/bin/env python

#Import Modules
import os
import sys
import socket
import threading
import Queue
import time
import shutil
import ftpserver
import tarfile
import glob
from PIL import Image
from daemon import Daemon

jobQueue = Queue.Queue(0)
taskQueue = Queue.Queue(0)
ftpFolder = '/var/ftp'
tempFolder = '/var/tmp/clusterTemp'
loggingFile = '/var/log/RenderServer.log'
pidFile = '/var/run/renderServer.pid'
ftpPort = 3457
serverPort = 5007

class ServerObj():

    def __init__(self):
        self.serverIP       = ''
        self.serverPort     = serverPort
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

class LoggingObj():

    def __init__(self):
        self.logFile = os.path.join(loggingFile)
        self.fileHandle = open(self.logFile, 'w')
        self.logFileLock = threading.Lock()

    def WriteLine(self, logLine):
        self.logFileLock.acquire()
        output = self.TimeStamp() + '  ' + str(logLine) + '\n'
        self.fileHandle.write(output)
        print output
        self.logFileLock.release()
    
    def TimeStamp(self):
        stamp = time.strftime("%Y%m%d-%H:%M:%S")
        return stamp


class FtpThread(threading.Thread):

    def run(self):

        LogFile.WriteLine('Starting ftp server')
        
        authorizer = ftpserver.DummyAuthorizer()
        
        authorizer.add_user('node', 'cluster', ftpFolder, perm='elradfmw')
        authorizer.add_user('client', 'cluster', ftpFolder, perm='elradfmw')

        ftp_handler = ftpserver.FTPHandler
        ftp_handler.authorizer = authorizer

        ftp_handler.banner = 'Nebula Cluster FTP Server'

        address = ('', ftpPort)
        ftpd = ftpserver.FTPServer(address, ftp_handler)

        ftpd.max_cons = 256
        ftpd.max_cons_per_ip = 5

        LogFile.WriteLine('Ftp server seems fine')
        
        ftpd.serve_forever()
        

class ClientThread(threading.Thread):

    def __init__(self, newSocket):
        self.clientSocket = newSocket
        self.running  = True
        threading.Thread.__init__(self)
    
    def run(self):
        self.Handshake()
        LogFile.WriteLine('Client Thread: client thread running')
        while self.running:
            self.GetClientInfo()

    def Handshake(self):
        self.clientSocket.send('connected')

    def GetClientInfo(self):
        try:
            fileName = self.clientSocket.recv(1024)
            if fileName == 0 or fileName == '':
                print 'problem here'
                self.running = False
                return 0
            LogFile.WriteLine('Client Thread: client sent ' + fileName)
            tarFileName = fileName + '.tar.gz'
            ftpFile = os.path.join(os.getcwd(), ftpFolder, tarFileName)
            if os.path.isfile(ftpFile):
                LogFile.WriteLine('Client Thread: file is on ftp server')
                taskQueue.put(fileName)
                LogFile.WriteLine('Client Thread: task has been put in queue')
            else:
                LogFile.WriteLine('Client Thread: file was not found on ftp server')
        except socket.error, msg:
            LogFile.WriteLine('Client Thread: client has disconnected')
            self.running = False



class PicJobGen():

    def __init__(self, InputFile, OutputFile, TaskFile, JobNumber, Height, Width, Other):
        self.taskFile      = TaskFile

        self.tempImagesDir = os.path.join(os.getcwd(), ftpFolder, self.taskFile + 'images')
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
        LogFile.WriteLine('Job Generator: creating ' + str(self.jobNumber) + ' picture jobs')
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
            LogFile.WriteLine('Job Generator: created job ' + str(jobInfo))
            jobQueue.put(jobInfo)
    
    def TaskFinish(self):
        LogFile.WriteLine('Job Generator: joining image slices')
        mainDir = os.getcwd()
        os.chdir(self.tempImagesDir)
        widthDiff = self.imageWidth / self.jobNumber
        blankCanvas = Image.new('RGB',(self.imageWidth,self.imageHeight))
        
        for inFile in glob.glob(self.outputFile + '_*.png'):
            file, ext = os.path.splitext(inFile)
            LogFile.WriteLine('Job Generator: slice join name ' + str(file))
            taskName,fileNumber = file.split('_')
            section = Image.open(inFile)
            xval = int(self.imageWidth * float(fileNumber))
            slicepos = (xval,0,xval + widthDiff,self.imageHeight)
            LogFile.WriteLine('Job Generator: slice position ' + str(slicepos))
            imageSlice = section.crop(slicepos)
            blankCanvas.paste(imageSlice,slicepos)
        blankCanvas.save(self.outputFile + '.png','PNG')
        os.chdir(mainDir)
        # Join image files together that have been uploaded to the ftp

    def TaskCleanUp(self):
        tempDir = os.path.join(os.getcwd(), tempFolder, self.taskFile)
        shutil.rmtree(tempDir)


class SequenceObj():

    def __init__(self, varName, varSequence, framesP16th):
        self.VarName = varName
        self.varSequence = self.seqConvert(varSequence)
        self.bpm = 0
        self.frm = 0
        self.length = 0
        self.framesP16th = framesP16th
        
        self.sectionCount = 0
        self.seqCount = 0
        self.repeat   = 0
        self.repVal   = 0

    def seqConvert(self, seqList):
        startVal,curve,meh = seqList[0]
        prevVal      = float(startVal)
        prevcurve    = float(curve)
        if prevcurve > 1:
            prevcurve = 1
        elif prevcurve < 0:
            prevcurve = 0
        prevPos = 0
        newSeq = []
        
        for data in seqList[1:]:
            value,curve,position = data
            newValue    = float(value)
            newcurve    = float(curve)
            if newcurve > 1:
                newcurve = 1
            elif newcurve < 0:
                newcurve = 0

            posBars, posBeats, posTeenths = position.split('.')
            teenthVal = (int(posBars) * 16) + (int(posBeats) * 4) + (int(posTeenths))
            
            secLength = int(self.framesP16th * (teenthVal - prevPos))
            delta = (newValue - prevVal)
            newSeq.append((prevVal,delta,secLength,prevcurve))
            prevVal   = newValue
            prevPos   = teenthVal
            prevcurve = newcurve
            
        return newSeq

    def SeqVal(self):
        if not self.repeat:
            start, delta, length, curve = self.varSequence[self.sectionCount]
            value = start + (delta * pow((self.seqCount / length),curve))
            self.seqCount += 1
            if self.seqCount == length:
                self.sectionCount += 1
                self.seqCount = 0
            if self.sectionCount == len(self.varSequence):
                self.repeat = 1
                self.repVal = value
            return value
        else:
            return self.repVal
        

class MovJobGen():

    def __init__(self, InputFile, OutputFile, TaskFile, Height, Width, Other):
        self.taskFile = TaskFile
 
        self.tempImagesDir = os.path.join(os.getcwd(), ftpFolder, self.taskFile + 'images')
        if not os.path.exists(self.tempImagesDir):
            os.mkdir(self.tempImagesDir)

        self.inputFile = InputFile
        self.outputFile = OutputFile
        self.imageHeight = Height
        self.imageWidth = Width
        self.otherParams = Other
        self.varList  = []
        self.varParams = {}
        
        
        LogFile.WriteLine('Task Thread: reading sequence file')
        paramFile = open(os.path.join(os.getcwd(), tempFolder, self.taskFile, 'seqFile.txt'))
        for line in paramFile:
            line = line.rstrip()
            line,params = line.split(':')
            if line == 'bpm':
                self.bpm = int(params)
            elif line == 'frm':
                self.frameRate   = int(params)
            elif line == 'len':
                self.length   = params
            elif line == 'varseq':
                varName,varSeqVals   = eval(params)
                self.varList.append(varName)
                self.varParams[varName] = varSeqVals
        
        self.sequences    = None
        
        framesP16th = (16 * float(self.bpm)) / (60 * float(self.frameRate))

        posBars, posBeats, posTeenths = self.length.split('.')
        lengthTeenths = (int(posBars) * 16) + (int(posBeats) * 4) + (int(posTeenths))
        self.totalLength = lengthTeenths * framesP16th
        
        for variable in self.varList:
    
            variableSequence = self.varParams[variable]
            
            seqObj = SequenceObj(variable,variableSequence, framesP16th)
            seqObj.bpm = self.bpm
            seqObj.frm = self.frameRate
            seqObj.length = self.totalLength
            self.sequences[variable] = seqObj
        
    def CreateJobs(self):
        for job in range(totalLength):

            outputFileName = self.outputFile + '_' + str(job)
                    
            paramsList = []
            paramsList.append('+I' + self.inputFile)
            paramsList.append('+O' + outputFileName)
            paramsList.append('+H' + str(self.imageHeight))
            paramsList.append('+W' + str(self.imageWidth))
            paramsList.append(self.otherParams)
            
            for variable in varList:
                paramsList.append('Declare=' + str(variable) + '=' + str(sequences[variable].SeqVal()))
            
            jobInfo = self.taskFile + '::' + outputFileName + '::' + ' '.join(paramsList)
            jobQueue.put(jobInfo)
    
    def TaskFinish(self):
        mainDir = os.getcwd()
        os.chdir(self.tempImagesDir)
        # Code to join single frames into movie goes here
        os.chdir(mainDir) 
 
 
    def TaskCleanUp(self):
        tempDir = os.path.join(os.getcwd(), 'temp', self.taskFile)
        shutil.rmtree(tempDir)

class TaskThread(threading.Thread):

    def __init__(self):
        self.running       = True
        
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
        LogFile.WriteLine('Starting up Task thread')
        
        threading.Thread.__init__(self)

    def run(self):
        
        while self.running:
            LogFile.WriteLine('Task Thread: waiting for task')
            self.GetTask()
            LogFile.WriteLine('Task Thread: got task ' + str(self.taskFile))
            self.ReadParams()
            LogFile.WriteLine('Task Thread: creating jobs')
            self.jobCreator.CreateJobs()
            LogFile.WriteLine('Task Thread: waiting for job queue to be empty')
            jobQueue.join()
            LogFile.WriteLine('Task Thread: task finished')
            self.jobCreator.TaskFinish()
            LogFile.WriteLine('Task Thread: cleaning up')
            self.jobCreator.TaskCleanUp()

    def GetTask(self):
        queueing = True
        while queueing:
            taskInfo = taskQueue.get()
            if taskInfo != None:
                self.taskFile = taskInfo
                queueing = False
            else:
                time.sleep(10)

    def ReadParams(self):
        self.tarName = os.path.join(os.getcwd(), ftpFolder, self.taskFile + '.tar.gz')
        tarFile = tarfile.open(self.tarName, mode = 'r:gz')
        tarFile.extractall(tempFolder)
        tarFile.close()
        LogFile.WriteLine('Task Thread: reading parameters file')
        paramFile = open(os.path.join(os.getcwd(), tempFolder, self.taskFile, 'params.cfg'))
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
            LogFile.WriteLine('Task Thread: rendering a picture')
            self.jobCreator = PicJobGen(self.inputFile, self.outputFile, self.taskFile, self.jobNumber, self.imageHeight, self.imageWidth, self.otherParams)
        elif self.renderType == 'movie':
            self.jobCreator = MovJobGen(self.inputFile, self.outputFile, self.taskFile, self.imageHeight, self.imageWidth, self.otherParams)
            LogFile.WriteLine('Task Thread: rendering a video')
        LogFile.WriteLine('Task Thread: finished reading parameters')



class NodeThread(threading.Thread):

    def __init__(self, newSocket, connectionIP):
        self.nodeIP = connectionIP
        self.nodeSocket = newSocket
        self.jobParams  = None
        self.running    = False
        threading.Thread.__init__(self)
        # create a thread for a particular socket

    def run(self):
        self.running = self.Handshake()
        LogFile.WriteLine(self.name + ': up and running for IP ' + str(self.nodeIP))
        while self.running:
            self.GetJob()
            if self.jobParams != None:
                self.RunJob()
            else:
                LogFile.WriteLine(self.name + ': Round again')

    def Handshake(self):
        try:
            connectCheck = self.nodeSocket.send('connected')
            if connectCheck == 0:
                return False
            else:
                return True
        except socket.error, msg:
            LogFile.WriteLine(self.name + ': Connection dropped, killing thread')
            return False

    def GetJob(self):
        queueing = True
        while queueing:
            LogFile.WriteLine(self.name + ': looking for jobs')
            self.jobParams = jobQueue.get()
            LogFile.WriteLine(self.name + ': should have a job now')
            queueing = False

    def RunJob(self):
        LogFile.WriteLine(self.name + ': got a job to run')
        LogFile.WriteLine(self.name + ': job info ' + self.jobParams )
        self.nodeSocket.send('jobs available')
        nodeInfo = self.nodeSocket.recv(1024)
        if nodeInfo == '':
            self.running = False
            LogFile.WriteLine(self.name + ': node failed on job ' + self.jobParams)
            jobQueue.put(self.jobParams)
            LogFile.WriteLine(self.name + ': putting job back into job queue')
            jobQueue.task_done()
            return False
        if nodeInfo == 'info':
            LogFile.WriteLine(self.name + ': remote node is ready for job')
            self.nodeSocket.send(self.jobParams)
            jobRunning = True
            while jobRunning:
                LogFile.WriteLine(self.name + ': remote node is running job')
                jobStatus = self.nodeSocket.recv(1024)
                if jobStatus == 'Completed':
                    LogFile.WriteLine(self.name + ': remote node has completed job')
                    jobQueue.task_done()
                    jobRunning = False
                elif nodeInfo == '':
                    self.running = False
                    LogFile.WriteLine(self.name + ': node failed on job ' + self.jobParams)
                    jobQueue.put(self.jobParams)
                    LogFile.WriteLine(self.name + ': putting job back into job queue')
                    jobQueue.task_done()
                    return False


class ServerDaemon(Daemon):
    
    def run(self):
        
        global LogFile
        LogFile = LoggingObj()

        LogFile.WriteLine('\n\n')
        LogFile.WriteLine('Cluster Server Starting Up')
        LogFile.WriteLine('')
        
        LogFile.WriteLine('Checking that all necesarry folders are available')
        
        if not os.path.exists(ftpFolder):
            os.mkdir(ftpFolder)
        if not os.path.exists(tempFolder):
            os.mkdir(tempFolder)
        
        ClusterServer = ServerObj()
        
        LogFile.WriteLine('Cluster Server running')
        
        ftpServer = FtpThread()
        ftpServer.daemon = True
        ftpServer.start()

        taskHandler = TaskThread()
        taskHandler.daemon = True
        taskHandler.start()
        
        LogFile.WriteLine('Serving Network requests on port ' + str(ClusterServer.serverPort))
        ClusterServer.CreateSocket()
        
        nodeNumber = 1
        
        while True:
        
            newSocket, address = ClusterServer.serverSocket.accept()
            newSocket.setblocking(1)
            socketType = newSocket.recv(1024)
            
            if socketType == 'node':
                LogFile.WriteLine('Node connection from ' + str(address))
                nodeHandler = NodeThread(newSocket, address)
                nodeHandler.daemon = True
                nodeHandler.name = 'Node Thread ' + str(nodeNumber)
                nodeNumber += 1
                LogFile.WriteLine('Created ' + str(nodeHandler.name) + ' for address ' + str(address))
                nodeHandler.start()
            elif socketType == 'client':
                LogFile.WriteLine('Client connection from ' + str(address))
                clientHandler = ClientThread(newSocket)
                clientHandler.daemon = True
                clientHandler.start()



if __name__ == "__main__":

    daemon = ServerDaemon(pidFile)
    
    if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                    daemon.start()
            elif 'foreground' == sys.argv[1]:
                    daemon.run()
            elif 'stop' == sys.argv[1]:
                    daemon.stop()
            elif 'restart' == sys.argv[1]:
                    daemon.restart()
            else:
                    print "Unknown command"
                    sys.exit(2)
            sys.exit(0)
    else:
            print "usage: %s start|stop|restart" % sys.argv[0]
            sys.exit(2)
                

