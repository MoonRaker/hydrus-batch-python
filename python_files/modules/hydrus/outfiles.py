#OUT_Class.py
#Created by Derek Groenendyk
#3/2/2010
#This a class that accesses the files with the Extension .OUT

import os
from Tkinter import *
import tkMessageBox
import numpy as np


class TLEVEL:
    
    def __init__(self,directory):
        
        self.directory = directory
        os.chdir(self.directory)
        self.dirList = os.listdir(self.directory)
        #Soil file of interest
        self.OUT_index = self.dirList.index("T_LEVEL.OUT")
        
        self.readLines()
       
    def update(self):
        self.dirList = os.listdir(self.directory)
        self.OUT_index = self.dirList.index("T_LEVEL.OUT")
        
        self.readLines()

    def readLines(self):
        #reads in the lines of the T_LEVEL file
        infile = open(self.directory+"\\"+self.dirList[self.OUT_index],"r")
        self.lines = infile.readlines()
        infile.close()

        self.headingData = []
        self.timeData = []

        line = self.lines[5].split()  # 6?
        for i in range(len(line)):
            heading = line[i]
            self.headingData.append(heading)
        
        for i in range(8,len(self.lines)): # 9?
            if self.lines[i].split()[0] == 'end': break
            time = float(self.lines[i].split()[0])
            self.timeData.append(time)

    def getData(self,time,heading):
        lindex = time+8 # 9?
        hindex = self.headingData.index(heading)
        paramValue = float(self.lines[lindex].split()[hindex])

        return paramValue

    def getNumTimes(self):
        return len(self.timeData)

    def getTimes(self):
        return self.timeData
    
    def getHeadings(self):
        return self.headingData


    def getLines(self,time,returnHeading=False,hasHeading=True,isEnd=False):
        if hasHeading:
            start = 8
        else:
            start = 4

        for i in range(start,len(self.lines)):
            if float(self.lines[i].split()[0]) == float(time):
                lines = self.lines[start:i+1]
                if isEnd:
                    lines = self.lines[start:i+2]
                break

        if returnHeading:
            for i in range(8):
                lines.insert(0,self.lines[7-i])
        return lines


class BALANCEOUT:
    
    def __init__(self,directory):
        
        self.directory = directory
        os.chdir(self.directory)
        self.dirList = os.listdir(self.directory)
        #Soil file of interest
        self.OUT_index = self.dirList.index("BALANCE.OUT")
        
        self.readLines()
       
    def update(self):
        self.dirList = os.listdir(self.directory)
        self.OUT_index = self.dirList.index("BALANCE.OUT")
        
        self.readLines()

    def readLines(self):
        #reads in the lines of the BALANCE file
        infile = open(self.directory+"\\"+self.dirList[self.OUT_index],"r")
        self.lines = infile.readlines()
        infile.close()

        self.headingData = []
        lastLines = []

        #creates the fieldData list with fieldCodes and the starting line number            
        for i in range(1,len(self.lines)):
            #why is this necessary: self.lines[i].find("*") >= 0, could just use == 0 ?
            if len(self.lines[i].split()) > 0:
                if self.lines[i].split()[0] == "Time":
                    heading = float(self.lines[i].split()[2])
                    self.headingData.append([heading, i, i+4,i+9])
        self.headingData = np.array(self.headingData)

    def getData(self,heading,param):
        for data in self.headingData:
            if data[0] == heading:
                firstLine = int(data[2])
                lastLine  = int(data[3])
                time = data[0]
        for i in range(firstLine,lastLine+1):
            if len(self.lines[i]) > 0:
                if param in self.lines[i]:
                    if heading == time:
                        paramValue = float(self.lines[i][20:32])
                        break

        return paramValue

    def getNumTimes(self):
        return self.headingData[:,0]


class NODINF:

    def __init__(self,directory):
        
        self.directory = directory
        os.chdir(self.directory)
        self.dirList = os.listdir(self.directory)
		
        #Soil file of interest
        self.OUT_index = self.dirList.index('NOD_INF.OUT')
        
        self.readData()
        
    def readData(self):

        infile = open(self.directory+"\\"+self.dirList[self.OUT_index],"r")
        self.lines = infile.readlines()
        infile.close()

        self.times = []

        for i in range(len(self.lines)):
            if len(self.lines[i]) > 1:
                if self.lines[i].split()[0] == 'Time:':
                    start = i
                elif self.lines[i][:-1].split()[0] == 'end':
                    end = i
                    break
        self.step = end - start + 3
        self.numTimes = (len(self.lines)-10)/self.step

        if 'Welcome' in self.lines[1].split():
            offset = 6
        elif 'Welcome' in self.lines[2].split():
            offset = 7
            
        for i in range(self.numTimes+1):
            self.times.append(offset+i*self.step)   
        self.firstNodes = np.array(self.times) + 6  # 6 == depth 0, 7 == depth 1

    def getTimes(self):
        return self.times

    def getNumTimes(self):
        return self.numTimes

    def getfirstNodes(self):
        return self.firstNodes

    def getAvgHeadData(self,depth):
        
        # column 6: flux
        
        self.averageHead = []
        
        for i in range(self.numTimes+1):
            total = 0 
            for j in range(depth):
                total += float(self.lines[self.firstNodes[i]+j+1].split()[2]) # the +1 accounts for the surface layer
            self.averageHead.append(total/depth)
            
        return self.averageHead

    def getWCRange(self,layers):
        
        # column 6: flux
        
        self.WC = np.zeros((self.numTimes+1,len(layers)))
        
        for i in range(self.numTimes+1):
            for j in layers:
                self.WC[i,j] = float(self.lines[self.firstNodes[i]+j].split()[3])
            
        return self.WC

    def calcDayIndex(self,time):
##        time = round((5/self.numTimes)*day,3)

        # print(self.times)
        # print(self.lines[self.times[-1]])

        endTime = float(self.lines[self.times[-1]].split()[-1])
        # print(time,endTime)

        self.timeIndex = int(round(self.numTimes*(time/endTime)))
        # print self.timeIndex

        return self.timeIndex       

    def getHeadData(self,day,stopLine=None):
        if day == 'end':
            dayIndex = len(self.firstNodes)-1
        else:
            dayIndex = self.calcDayIndex(day)
            # dayIndex = float(day)
        headList = []
        i = -1
        end = None
        while end != 'end':
            i += 1
            index = self.firstNodes[dayIndex] + i  + 1 # the +1 accounts for the surface layer
            line = self.lines[index]
            headList.append(float(line.split()[2]))
            end = self.lines[index+1].split()[0]
            if self.lines[index].split()[0] == str(stopLine + 1):
                end = 'end'
        return np.array(headList)
    
    def getWCData(self,day,stopLine=None):

        if day == 'end':
            dayIndex = len(self.firstNodes)-1
        else:
##        dayIndex = self.calcDayIndex(day)
            dayIndex = float(day)

        WCList = []
        i = -1
        end = None
        while end != 'end':
            i += 1
            index = self.firstNodes[dayIndex] + i + 1 # the +1 accounts for the surface layer
            line = self.lines[index]
            WCList.append(float(line.split()[3]))
            end = self.lines[index+1].split()[0]
            if self.lines[index].split()[0] == str(stopLine + 1):
                end = 'end'
        return np.array(WCList)
    
    def removeData(self,numNodes):

        temp = []
        for i in range(self.times[0]+6+numNodes):
            if len(self.lines[i]) > 71:
                temp.append(self.lines[i][:71]+'\n')
            else:
                temp.append(self.lines[i])
        temp.append('end\n\n\n')
        
        for i in self.times[1:]:
            startLine = i
            endLine = i + 6 + numNodes
            for j in range(startLine,endLine):
                try:
                    if len(self.lines[j]) > 71:
                        temp.append(self.lines[j][:71]+'\n')
                    else:
                        temp.append(self.lines[j])
                except IndexError:
                    print j
            temp.append('end\n\n\n')
                    
        self.lines = temp
        self.writeData()

    def getFlux(self,time,layer):
        index = self.firstNodes[time] + layer - 1
        return float(self.lines[index].split()[6])

    def writeData(self):

        outfile = open(self.directory+"\\"+self.dirList[self.OUT_index],"w")
        outfile.seek(0,0)                    
        outfile.writelines(self.lines)
        outfile.close()

    def getLines(self,time,heading=False):
        
        for index in self.times:
            if float(self.lines[index].split()[1]) == float(time):
##                print float(self.lines[index].split()[1]),float(time),self.step
                lines = self.lines[index:index+self.step]
                break

        if heading:
            for i in range(6):
                lines.insert(0,self.lines[5-i])
                             
        return lines
        

class PROFILEOUT:

    def __init__(self,directory):
        
        self.directory = directory
        os.chdir(self.directory)
        self.dirList = os.listdir(self.directory)
        #Soil file of interest
        self.OUT_index = self.dirList.index('PROFILE.OUT')
        
        self.readData()
        
    def readData(self):

        infile = open(self.directory+"\\"+self.dirList[self.OUT_index],"r")
        self.lines = infile.readlines()
        infile.close()


    def removeData(self,numNodes):
                  
        self.lines = self.lines[:9 + numNodes]
        self.lines.append('end\n')
        self.writeData()


    def writeData(self):

        outfile = open(self.directory+"\\"+self.dirList[self.OUT_index],"w")
        outfile.seek(0,0)                    
        outfile.writelines(self.lines)
        outfile.close()


class ENSEMBLEOUT:

    def __init__(self,directory):
        
        self.directory = directory
        os.chdir(self.directory)
        self.dirList = os.listdir(self.directory)
        #Soil file of interest
        self.OUT_index = self.dirList.index('ENSEMBLE.OUT')
        
        self.readData()
        
    def readData(self):

        infile = open(self.directory+"\\"+self.dirList[self.OUT_index],"r")
        self.lines = infile.readlines()
        infile.close()

        paramDict = {'*Q':N,'*R':M,'*A':N,'*H':M,'*K':N,'*xapriori':N,'*xaposteriori':N,'*residual':N,'*papriori':N,'*paposteriori':N}

        paramValues = []

        for param in paramDict.Keys:
            for i in range(len(self.lines)):
                if len(self.lines[i]) > 0:
                    line = self.lines[i].split()
                    if param in line:
                        numCols = self.lines[i+1].split(',')
                        data = np.zeros((paramDict[param],numCols))
                        for j in range(paramDict[param]):
                            data[j,:] = [float(item) for item in self.lines[i+1+j].split(',')]
                        paramValues.append(data)
                        break

        self.data = zip(paramDict.Keys,paramValues)


    def getData(self,param):
        for data in self.data:
            if data[0] == param:
                paramValue = data[1]

        return paramValue 
            



class DATAOUT:

    def __init__(self,directory):
        
        self.directory = directory
        os.chdir(self.directory)
        self.dirList = os.listdir(self.directory)
        #Soil file of interest
        self.OUT_index = self.dirList.index('DATA.OUT')
        
        self.readData()
        
    def readData(self):

        infile = open(self.directory+"\\"+self.dirList[self.OUT_index],"r")
        self.lines = infile.readlines()
        infile.close()

        paramDict = {'t':0.0}

        paramValues = []

        for param in paramDict.keys():
            for i in range(len(self.lines)):
                if len(self.lines[i].split()) > 0:
                    if self.lines[i].split()[0] == param:
                        paramValues.append(self.lines[i].split()[1])
                        break
                    
        self.data = zip(paramDict.keys(),paramValues)


    def getData(self,param):
        for data in self.data:
            if data[0] == param:
                paramValue = data[1]
        return paramValue 


class ICHECK:
    
    def __init__(self,directory):
        
        self.directory = directory
        os.chdir(self.directory)
        self.dirList = os.listdir(self.directory)
        #Soil file of interest
        self.OUT_index = self.dirList.index("I_CHECK.OUT")
        infile = open(self.directory+"\\"+self.dirList[self.OUT_index],"r")
        self.lines = infile.readlines()
        infile.close()

        self.findHeaders()


    def getMatN(self,node):

        start = 15
        
        if self.NodalEnd - start > node:
            matNum = int(self.lines[node+start].split()[3])
            return matNum
        else:
            print "There isn't that many nodes..."

    def getParams(self,node):

        matNum = self.getMatN(node)
        
        for i in range(self.MatNumStart,self.MatNumEnd+1):
            line = self.lines[i].split()
            if int(line[0]) == matNum:
                paramData = [float(line[j+1]) for j in range(5)]
                break
        paramList = ['thr','ths','Alfa','n','Ks']
        params = dict(zip(paramList,paramData))

        return paramData   


    def findHeaders(self):

        for i in range(len(self.lines)):
            if len(self.lines[i].split()) > 0:
                if self.lines[i].split()[0] == 'Nodal':
                    self.NodalStart = i+4
                elif self.lines[i].split()[0] == 'MatNum,':
                    self.MatNumStart = i+4
                    self.NodalEnd = i-6
                elif self.lines[i].split()[0] == 'Table':
                    self.MatNumEnd = i-2            

 








