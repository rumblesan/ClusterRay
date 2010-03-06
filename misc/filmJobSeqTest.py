#!/usr/bin/env python

#Import Modules
import os

bpm = None
frameRate = None
seqParams = None
length = None
varList = []
varParams = {}

sequences = {}



class SequenceObj():

    def __init__(self,varName, varSequence):
        self.VarName = varName
        self.varSequence = self.seqConvert(varSequence)
        self.bpm = 0
        self.frm = 0
        self.length = 0
        
        self.sectionCount = 0
        self.seqCount = 0
        self.repeat   = 0
        self.repVal   = 0

    def seqConvert(self, seqList):
        startVal,meh = seqList[0]
        prevVal = float(startVal)
        prevPos = 0
        newSeq = []
        
        for data in seqList[1:]:
            value,position = data
            newValue = float(value)
            
            posBars, posBeats, posTeenths = position.split('.')
            teenthVal = (int(posBars) * 16) + (int(posBeats) * 4) + (int(posTeenths))
            
            secLength = int(framesP16th * (teenthVal - prevPos))
            delta = (newValue - prevVal) / (secLength - 1)
            newSeq.append((prevVal,delta,secLength))
            prevVal = newValue
            prevPos = teenthVal
            
        return newSeq

    def SeqVal(self):
        if not self.repeat:
            start, delta, length = self.varSequence[self.sectionCount]
            value = start + (delta * self.seqCount)
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
        
        


paramFile = open('seqFile.txt')
for line in paramFile:
    line = line.rstrip()
    line,params = line.split(':')
    if line == 'bpm':
        bpm = int(params)
    elif line == 'frm':
        frameRate   = int(params)
    elif line == 'len':
        length   = params
    elif line == 'varseq':
        varName,varSeqVals   = eval(params)
        varList.append(varName)
        varParams[varName] = varSeqVals


paramFile.close()

framesP16th = (16 * float(bpm)) / (60 * float(frameRate))

posBars, posBeats, posTeenths = length.split('.')
lengthTeenths = (int(posBars) * 16) + (int(posBeats) * 4) + (int(posTeenths))
totalLength = lengthTeenths * framesP16th

for variable in varList:
    
    variableSequence = varParams[variable]
    
    seqObj = SequenceObj(variable,variableSequence)
    seqObj.bpm = bpm
    seqObj.frm = frameRate
    seqObj.length = totalLength
    sequences[variable] = seqObj


for i in range(totalLength):

    line = []

    for variable in varList:
        line.append(sequences[variable].SeqVal())
    print line






