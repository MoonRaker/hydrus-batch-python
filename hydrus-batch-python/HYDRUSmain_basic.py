## HYDRUSmain.py
## Written by Derek Groenendyk
## 03/30/2012
## updated 03/30/2015
## Calls and modifies CropModel project

from hydrusEXE import *
from utils.wc import *
from hydrus.infiles import *
from hydrus.outfiles import *

from time import clock
import time
import shutil
import os
import numpy
from time import clock
import scipy as sp
import numpy as np
import sys
import cPickle


def run():

    srcDrive = "C:\\Derek\\"

    method = 2 # 1 = Single HYDRUS run, 2 = Many Runs

    # Name of experiment
##    exp = 'SimpleEnsemble'
##    exp = 'Test'
    # exp = 'CropModel'
##    exp = 'HWRS_642'
##    exp = 'AGU_Assim'
##    exp = 'MatNumTest'
##    exp = 'Phillips'

    exp = 'SW605_FreeDrainage'
    # exp = 'SW605_InfOnly'
    # exp = 'SW605'
    
    # Experiment File location
    ExpFileLocation = srcDrive+"ProgrammingFolder\\HYDRUS_Data\\Projects\\"+exp
    noCMDWindow = 1
    
    numLayers = 211
    
    fileExtList = [".out",".in",".txt",".dat",".pkl"]

    #Initialize Classes
    hydrusEXE = HYDRUS(ExpFileLocation,exp)

    startTime = time.clock()

    # Run one simulation of the project
    if method == 1:      

        # paramDict = {'lSink':'f','lRoot':'f'}
        # setSelectorParams(ExpFileLocation,paramDict)

        # paramDict = {'MaxIt':20,'TolH':1,'Model':0}#,'hTabN':0,'hTab1':0}
        # setSelectorParams(ExpFileLocation,paramDict)

        paramValues = getAllTexParams()
        paramList = ['thr','ths','Alfa','n','Ks']

        soil = 747   # DSSAT Wheat Soil top ~90-100 cm, [34,32,34], 747

        for i in range(len(paramList)):
            data = [str(paramValues[soil,i])] 
            setSelectorParams(ExpFileLocation,{paramList[i]:data},nmat=1)
            
        hydrusEXE.run_hydrus(noCMDWindow,str(1))
        hydrusEXE.outputResults("Crop - Homogeneous",str(soil))
        print('Done...')

    # Run multiple simulations of HYDRUS
    elif method == 2:

        paramDict = {'lSink':'f','lRoot':'f','hTabN':100000}        
        setSelectorParams(ExpFileLocation,paramDict)

        paramValues = getAllTexParams()
        numSoils = 1326

        for ind in range(numSoils):
            soil = ind
            print('###############################')
            print('Soil: ' + str(soil))
            print('###############################')
                             
            # set varying parameters
            paramList = ['thr','ths','Alfa','n','Ks']
            for i in range(len(paramList)):
                data = [str(paramValues[soil,i])]
                setSelectorParams(ExpFileLocation,{paramList[i]:data})

            hydrusEXE.run_hydrus(noCMDWindow,str(1))
            fileLocation = hydrusEXE.outputResults("ROSETTA - 2 Percent - Test",str(soil))

        print('Done...')

    # stopTime = time.clock()
    # lengthOfRun = stopTime - startTime
    # timeOfDay = time.localtime(time.time())
    # print('Took:   '+str(lengthOfRun)+' seconds,  Finished at:  '+str(timeOfDay[3])+':'+str(timeOfDay[4]))

def getAllTexParams():

    water = WC()
    paramValues = water.getParams()
    
    return paramValues

def getAllSSC():

    water = WC()
    paramValues = SSCData = water.getSSC() 

    return paramValues

def getSoilParams(ExpFileLocation):
    paramList = ['thr','ths','Alfa','n','Ks','l']

    incrementList = [1.0,0.95,0.90,1.05,1.10]
    numModels = len(incrementList)

    selectorIN = SELECTORIN(ExpFileLocation)
    numLayers = len(selectorIN.getData('thr'))
    paramValues = np.zeros((numModels,6,numLayers))
    for i in range(len(paramList)):
        data = selectorIN.getData(paramList[i]) #for all materials
        for j in range(numModels):
            if i == len(paramList) -1:
                increment = 1.0
            else:
                increment = incrementList[j]
            paramValues[j,i,:] = np.array([round(float(item)*increment,4) for item in data])

    return paramValues,numModels

def setSelectorParams(ExpFileLocation,paramDict,nmat = 1):

    selectorIN = SELECTORIN(ExpFileLocation)

    for param in paramDict.keys():
        selectorIN.setData(param,paramDict[param],mat = nmat)

    selectorIN.update()


def main():
    run()
             
if __name__ == "__main__":
    main()
       

        
