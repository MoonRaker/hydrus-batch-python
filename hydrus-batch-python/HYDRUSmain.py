## HYDRUSmain.py
## Written by Derek Groenendyk
## 03/30/2012
## Calls and modifies CropModel project

from hydrusEXE import *

# from IN_Class import *
# from OUT_Class import *
# from WC_Class import *
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
import pickle
from scipy.io import *


def runCropModel():
    srcDrive = "C:\\Derek\\"

    method = 3 # 1 = Single HYDRUS run, 2 = simple single run, 3 = Many Runs, ? = MonteCarlo, 4 = Ensemble

    expYear = '04'

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
    exp = 'SW605'

    # exp = 'SW605_2'
    

    # Experiment File location
    ExpFileLocation = srcDrive+"ProgrammingFolder\\HYDRUS_Data\\Projects\\"+exp
    noCMDWindow = 0
    
##    numDays = len(lines) - 6
##  CropModel    
    numDays = 208
    numLayers = 211
    
##  Simple Ensemble
##    numDays = 3
##    numLayers = 100

##  AGU Assimilation
##    numDays = 182
##    numDays = 5
##    numLayers = 201
    
    baseDirectory = srcDrive + "ProgrammingFolder\\CropModel\\" 

##    weatherFile = 'KSAS8101.WTH'
##    weatherFile = 'RORO7401.WTH'
##    weatherFile = 'AZMT0305.WTH'
    weatherFile = 'AZMT0305_withIrrigation.WTH'
##    weatherFile = 'AZMT0305_noIrrigation.WTH'

    weatherFile = baseDirectory + 'AZMT0305_withIrrigation.WTH'

    fileExtList = [".out",".in",".txt",".dat",".pkl"]

    #Initialize Classes
    hydrusEXE = HYDRUS(ExpFileLocation,exp)

    startTime = time.clock()

    # Run one simulation of the project
    if method == 1:

##        soilIndex = 579
##        
##        infile = open('newSoilProps.txt','r')
##        lines = infile.readlines()
##        infile.close()
##
##        paramValues = water.getParams()
##                
##        paramList = ['thr','ths','Alfa','n','Ks']
##        for j in range(len(paramList)):
##            paramValue = paramValues[soilIndex,j]
##        
##        nodInf = NODINF(ExpFileLocation)
##        nodInf.removeData(55)
##        profile = PROFILE(ExpFileLocation)
##        profile.removeData(55)        
                
        setMeteo(srcDrive,ExpFileLocation,weatherFile,numDays,iRadiation=2,iCrop=0)
        paramDict = {'lSink':'f','lRoot':'f','iAssim':0,'CropType':0,'Ensemble':'f'}

##        paramDict = {'lPrintD':'f','nPrintSteps':1,'tPrintInterval':1,'lEnter':'f',
##                 'TPrint(1),TPrint(2),...,TPrint(MPL)':np.arange(numDays)+1,
##                 'tMax':numDays,'tInit':0,'MPL':numDays,
##                 'iAssim':0,'CropType':1,'Trial':0,'Ensemble':'f','NMat':1}
        setSelectorParams(ExpFileLocation,paramDict)

        paramDict = {'MaxIt':20,'TolH':1,'Model':0}#,'hTabN':0,'hTab1':0}
        setSelectorParams(ExpFileLocation,paramDict)


##        profile = PROFILEDAT(ExpFileLocation)
##        profile.setData('Mat',1)
##        for i in range(500):  # 500 soils
##            profile.setData('Mat',i+1,layer=i)

##        selectorIN = SELECTORIN(ExpFileLocation)
##        selectorIN.addMat(numMat=500)

        paramValues = getAllTexParams()
##        print tempParams[746,:]
##        paramValues = np.repeat([tempParams[746,:]],500,axis=0)
##        print paramValues.shape
        paramList = ['thr','ths','Alfa','n','Ks']
##        for soil in range(500):  # 500 soils

        soil = 747   # DSSAT Wheat Soil top ~90-100 cm, [34,32,34], 747
##        soil = 712 #1313,1303

        for i in range(len(paramList)):
            data = [str(paramValues[soil,i])] 
##            if paramList[i] == 'Ks':
##                data[0] = round(float(data[0])/(24.0*60.0),7)  # coverts to cm/min, Phillips Experiment
            setSelectorParams(ExpFileLocation,{paramList[i]:data},nmat=1)
##            setSelectorParams(ExpFileLocation,{paramList[i]:data},nmat=soil+1)  # multiple soils
            
        hydrusEXE.run_hydrus(noCMDWindow,str(1))
##        hydrus.outputResults("MOSCEM4",str(1))
##        hydrus.outputResults("ManualDataParams",str(1))
##        hydrus.outputResults("M_RosettaSoils",str(1))
##        hydrus.outputResults("M_RosettaQSoils",str(1))
##        hydrus.outputResults("M_DSSATSoils",str(1))
##        hydrus.outputResults("Wheat - Optimized",str(1))
        hydrusEXE.outputResults("Crop - Homogeneous",str(soil))
        print('Done...')

        
    elif method == 2:
        setMeteo(srcDrive,ExpFileLocation,weatherFile,numDays,iRadiation=2,iCrop=3)
        hydrusEXE.run_hydrus(noCMDWindow,str(1))

    # Run multiple simulations of HYDRUS
    elif method == 3:
        #  Make sure it is using the original SELECTOR.IN file

        paramValuesFull = getAllTexParams(perturb_prct="01")
        paramValues = getAllTexParams(prct='one',model='old')
        # numSoils = 4
        numSoils = paramValues.shape[0]

        # offset = 3953
        for k in range(1):
        # for k in range(1000-offset):
            k += offset
    ##        profile = PROFILEDAT(ExpFileLocation)
    ##        profile.setData('Mat',1)

            # setMeteo(srcDrive,ExpFileLocation,weatherFile,numDays,iRadiation=2,year=expYear,iCrop=0)            

    ##        paramDict = {'lShort':'t','lPrintD':'f','nPrintSteps':1,'tPrintInterval':1,'lEnter':'f',
    ##                     'iAssim':0,'CropType':1,'Ensemble':'f'}
            
    ##        paramDict = {'lSink':'t','lRoot':'t','iAssim':0,'CropType':1,'Ensemble':'f','hTabN':100000}
            paramDict = {'lSink':'f','lRoot':'f','iAssim':0,'CropType':0,'Ensemble':'f','hTabN':100000}
            
    ##        paramDict = {'lSink':'f','lRoot':'f','lPrintD':'f','nPrintSteps':1,'tPrintInterval':1,'lEnter':'f',
    ##                 'TPrint(1),TPrint(2),...,TPrint(MPL)':np.arange(numDays)+1,
    ##                 'tMax':numDays,'tInit':0,'MPL':numDays,
    ##                 'iAssim':0,'CropType':0,'Trial':0,'Ensemble':'f','NMat':1}
            
            setSelectorParams(ExpFileLocation,paramDict)
            
    ##        paramDict = {'MaxIt':20,'TolH':1,'Model':3}#,'hTabN':0,'hTab1':0} # need to fix model (in Water and Root)
            # setSelectorParams(ExpFileLocation,paramDict)
            
            # paramValuesK = paramValuesFull[k,:,:] ##

    ##        soils = [1,4,54,104,150,158,199,200,202,247,292,340,382,432,466,507,547,550,553,
    ##                 588,593,624,697,700,923,925,951,976,977,1297,1302]
    ##
    ##        numSoils = len(soils)

    ##        
    ##        soils = [746, 747, 779, 781, 677, 713, 641, 714, 676, 711, 639, 710, 678, 640, 712]
    ##        soils = [515, 516, 554, 556, 434, 476, 392, 477, 433, 474, 390, 473, 435, 391, 475]
    ##        numSoils = len(soils)

            
    ######  Prematurely ended trials - No Crop, 8/7/2013
    ##        soils = [929, 1321 , 1322 , 1323 , 1324, 1325]
    ######  Prematurely ended trials - Crop, 8/7/2013
    ##        soils = [1313, 1316, 1317, 1319, 1320, 1321 , 1322 , 1323 , 1324, 1325]
            
    ##        numSoils = len(soils)

            ###### Melissa Clutter  ##########################
            # numSoils = 10
            # infile = open('C:\Derek\ProgrammingFolder\precs.txt','r')
            # lines = infile.readlines()
            # infile.close()

            # print(lines[0])
            # print()
            # precs = [round(float(line.split(' ')[2]),2) for line in lines]

            # days = [31,28,31,30,31,30,31,31,31,31,30]

            for ind in range(numSoils):
    ##            soil = soils[ind]
                soil = ind + offset
                print('###############################')
                print('Soil: ' + str(soil))
                print('###############################')


                # numDays = days[ind]

                # setAtmosh(ExpFileLocation,precs[ind],numDays)
                # paramDict = {'tMax':numDays,'MPL':numDays,'TPrint(1),TPrint(2),...,TPrint(MPL)':np.arange(numDays)+1}
                # setSelectorParams(ExpFileLocation,paramDict)


                
    ##                paramDict = {'lPrintD':'f','nPrintSteps':1,'tPrintInterval':1,'lEnter':'f',
    ##                             'Ensemble':'f','iAssim':0,'CropType':1}
    ##                setSelectorParams(ExpFileLocation,paramDict)
                    
                #### set varying parameters
                paramList = ['thr','ths','Alfa','n','Ks']
                paramDict = dict(zip(['thr','ths','Alfa','n','Ks'],range(5)))

                data = [[str(paramValues[soil,paramDict[paramList[i]]])] for i in range(len(paramList))]
                dataDict = dict(zip(paramList,data))
                setSelectorParams(ExpFileLocation,dataDict)

                # for i in range(len(paramList)):
                # for i in [2]:
                    # data = [str(paramValuesK[soil,paramDict[paramList[i]]])]
                    # print(data)
                   # if paramList[i] == 'Ks':
                       # data[0] = round(float(data[0])/(24.0*60.0),7)  # coverts to cm/min, used for Phillip's simulations
                    # setSelectorParams(ExpFileLocation,{paramList[i]:data})

                hydrusEXE.run_hydrus(noCMDWindow)
    ##            nodInf = NODINF(ExpFileLocation)
    ##            nodInf.removeData(200)
    ##            fileLocation = hydrus.outputResults("Phillips - Test",str(soil))
    ##            fileLocation = hydrus.outputResults("Crop - 642 - Test",str(soil))
                # fileLocation = hydrus.outputResults("No Crop - Homogeneous",str(soil))
                # fileLocation = hydrusEXE.outputResults("Melissa",str(soil))
                # time.sleep(0.25)
                # fileLocation = hydrusEXE.outputResults("1 percent - new",str(soil))
                hydrusEXE.saveOutput(soil,exp,200,db="1 percent - old",numtrials=numSoils,trial=soil)

            # hydrusEXE.saveOutput(k,exp,200,'2 percent - test')
            print('Finished iteration: '+str(k))

        print('Done...')

    # Run the simulation in Ensemble Mode - SimpleEnsemble ( aka Normal Hydrus Simulation)
    elif method == 4:

##        setMeteo(srcDrive,ExpFileLocation,weatherFile,numDays,iRadiation=2)
        
        paramDict = {'lPrintD':'t','nPrintSteps':1,'tPrintInterval':1,'lEnter':'f',
                     'iAssim':0,'CropType':0,'Ensemble':'t'}
        setSelectorParams(ExpFileLocation,paramDict)

        for trial in range(numDays):          
            paramDict = {'TPrint(1),TPrint(2),...,TPrint(MPL)':np.arange(trial+1)+1,
                         'tMax':trial+1,'tInit':trial,'MPL':trial+1,'Trial':trial}
            setSelectorParams(ExpFileLocation,paramDict)
            
            if trial > 0:
##                updateProfileDAT(ExpFileLocation,numLayers) # not needed, hNew gets overwritten in HYDRUS
                updateEnsembleIN(ExpFileLocation,numLayers)
                
            print("Start of Trial ",trial,'... ')
            hydrus.run_hydrus(noCMDWindow,str(1))
            fileLocation = hydrus.outputResults("SimpleEnsemble\\Trials",str(trial))
            
        print('Done...')

    # Run the simulation in Ensemble Mode - CropModel
    elif method == 5:

        setMeteo(srcDrive,ExpFileLocation,weatherFile,numDays,iRadiation=2)
        
        paramDict = {'lPrintD':'f','nPrintSteps':1,'tPrintInterval':1,'lEnter':'f',
                     'iAssim':0,'CropType':1,'Ensemble':'t'}
        setSelectorParams(ExpFileLocation,paramDict) 

        for trial in range(numDays):           
            # update Selector.IN object
            paramDict = {'TPrint(1),TPrint(2),...,TPrint(MPL)':np.arange(trial+1)+1,
                         'tMax':trial+1,'tInit':trial,'MPL':trial+1,'Trial':trial}
            setSelectorParams(ExpFileLocation,paramDict)        
            
            if trial > 0:
##                updateProfileDAT(ExpFileLocation,numLayers) # not needed, hNew gets overwritten in HYDRUS
                updateEnsembleIN(ExpFileLocation,numLayers)

            print("Start of Trial ",trial,'... ')
            hydrus.run_hydrus(noCMDWindow,str(1))
            fileLocation = hydrus.outputResults("Ensemble\\Trials",str(trial))

        print('Done...')

    # Run the simulation in Ensemble Mode, multiple models
    elif method == 6:

        paramValues,numModels = getSoilParams(ExpFileLocation)
        setMeteo(srcDrive,ExpFileLocation,weatherFile,numDays,iRadiation=2,year=expYear)

        for trial in range(numDays):
            for model in range(numModels):    
                if trial == 0:
                    paramDict = {'lPrintD':'f','nPrintSteps':1,'tPrintInterval':1,'lEnter':'f',
                                 'Ensemble':'t','iAssim':0,'CropType':1}
                    setSelectorParams(ExpFileLocation,paramDict)
                    
                    # set varying parameters
                    paramList = ['thr','ths','Alfa','n','Ks','l']
                    for i in range(len(paramList)):
                        data = [str(item) for item in paramValues[model,i,:]]
                        setSelectorParams(ExpFileLocation,{paramList[i]:data})

                # move in files
                if trial > 0:
                    directory = srcDrive+"ProgrammingFolder\\HYDRUS_Data\\Projects\\Results\\"+exp+"\\Ensemble\\Simulation "+str(model)+"\\Trials\\Trial= "+str(trial-1)

                    moveEnsembleFiles(ExpFileLocation,directory)
                    updateEnsembleIN(ExpFileLocation,numLayers)

                    
                # create file Selector.IN object
                # 1:direct,2:KF,3:EnKF

                paramDict = {'TPrint(1),TPrint(2),...,TPrint(MPL)':np.arange(trial+1)+1,
                             'tMax':trial+1,'tInit':trial,'MPL':trial+1,
                             'Trial':trial,}
                setSelectorParams(ExpFileLocation,paramDict)

                print("Start of Trial ",trial,'... ')
                hydrus.run_hydrus(noCMDWindow,str(1))
                fileLocation = hydrus.outputResults("Ensemble\\Simulation "+str(model)+"\\Trials",str(trial))

        print('Done...')


    # runs the ensemble with assimilation
    elif method == 7:

        paramList = ['thr','ths','Alfa','n','Ks','l']

        paramValues,numModels = getSoilParams(ExpFileLocation)
        setMeteo(srcDrive,ExpFileLocation,weatherFile,numDays,iRadiation=2)

        paramDict = {'@DI':2,'NO':15,'NL':30,'OP':1,
                     'SL':1,'DT':2,'M':1,'N':5,'Q':0.0200,'R':0.0100,'ASSIMFILE....':'assimdata.txt'}
        setDataIN(ExpFileLocation,paramDict)
            
        for trial in range(numDays):
            for model in range(numModels):
                       
                if trial == 0:
                # create file Selector.IN object
                # 1:direct,2:KF,3:EnKF
                    paramDict = {'lPrintD':'f','nPrintSteps':1,'tPrintInterval':1,'lEnter':'f',
                                 'Ensemble':'t','iAssim':3,'CropType':1}
                    setSelectorParams(ExpFileLocation,paramDict)
                    
                    # set varying parameters
                    for i in range(len(paramList)):
                        data = [str(item) for item in paramValues[model,i,:]]
                        setSelectorParams(ExpFileLocation,{paramList[i]:data})

                # move in files
                if trial > 0:
                    directory = srcDrive+"ProgrammingFolder\\HYDRUS_Data\\Projects\\Results\\"+exp+"\\Ensemble\\Simulation "+str(model)+"\\Trials\\Trial= "+str(trial-1)

                    moveEnsembleFiles(ExpFileLocation,directory)
                    updateEnsembleIN(ExpFileLocation,numLayers)
                    updateAssimIN(ExpFileLocation)

                paramDict = {'TPrint(1),TPrint(2),...,TPrint(MPL)':np.arange(trial+1)+1,
                             'tMax':trial+1,'tInit':trial,'MPL':trial+1,'Trial':trial}
                setSelectorParams(ExpFileLocation,paramDict)
                    
                print("Start of Trial ",trial,'... ')
                hydrus.run_hydrus(noCMDWindow,str(1))
                fileLocation = hydrus.outputResults("Ensemble\\Simulation "+str(model)+"\\Trials",str(trial))

            # Calculate co-variances
            directory = srcDrive+"ProgrammingFolder\\HYDRUS_Data\\Projects\\Results\\"+exp+"\\Ensemble\\Simulation 0\\Trials\\Trial= 0"
            dirResults = srcDrive+"ProgrammingFolder\\HYDRUS_Data\\Projects\\Results\\"+exp+"\\Ensemble\\"

            calculateVariances(directory,numModels,trial,dirResults)

        print('Done...')

        
    # runs the ensemble with assimilation for a non-cropped HYDRUS
    elif method == 8:
        paramList = ['thr','ths','Alfa','n','Ks','l']

        paramValues,numModels = getSoilParams(ExpFileLocation)  # percentage change in params
        paramValues = getAllTexParams()   #  list of known soils params


        pkl_file = open('C:\\Derek\\CropModel\\soilsDict.pkl', 'rb')
        soilsDict = pickle.load(pkl_file)
        pkl_file.close()

        numModels = len(soilsDict)

        
##        setMeteo(srcDrive,ExpFileLocation,weatherFile,numDays,iRadiation=2)

##      For the EnKF probably don't need most of this
        
##        for model in range(numModels):
##            tempDirectory = "C:\\Derek\\CropModel\\AGU_Assim_EnsTemp\\Model= "+str(model)
##            try:
##                os.makedirs(tempDirectory)
##            except OSError:
##                shutil.rmtree(tempDirectory)
##                os.makedirs(tempDirectory)

            
        for trial in range(numDays):
            for model in range(numModels):
##                modelDirectory = "C:\\Derek\\CropModel\\AGU_Assim_EnsTemp\\Model= "+str(model)
##                shutil.copy2('C:\\Derek\\CropModel\\' + 'assimdata'+str(model)+'.txt', ExpFileLocation)
                       
                if trial == 0:
                # create file Selector.IN object
                # 1:direct, 2:KF, 3:EnKF
                    paramDict = {'lPrintD':'f','nPrintSteps':1,'tPrintInterval':1,'lEnter':'f',
                                 'Ensemble':'t','iAssim':3,'CropType':0}
                    setSelectorParams(ExpFileLocation,paramDict)
                    
                    paramDict = {'@DI':2,'NO':15,'NL':30,'OP':1,
                                 'SL':1,'DT':2,'M':1,'N':30,'Q':0.0200,'R':0.0100,'ASSIMFILE....':'assimdata'+str(model)+'.txt'}
                    setDataIN(ExpFileLocation,paramDict)

                    
##                    # set varying parameters # percentage change in params
##                    for i in range(len(paramList)):
##                        data = [str(item) for item in paramValues[model,i,:]]
##                        setSelectorParams(ExpFileLocation,{paramList[i]:data})

                    # set varying parameters  #  list of known soils params
                    paramList = ['thr','ths','Alfa','n','Ks']
                    soil = soilsDict.keys()[model]
                    for i in range(len(paramList)):
                        data = [str(paramValues[soil,i])] 
                        setSelectorParams(ExpFileLocation,{paramList[i]:data})

##                    os.chdir(ExpFileLocation)
##                    currentDir = os.curdir
##                    dirList = os.listdir(currentDir)
##                    fileExtList = [".OUT",".out",".IN",".TXT",".DAT"]
##                    INFILES = []
##                    for OUTFILE in dirList:
##                        if os.path.splitext(OUTFILE)[1] in fileExtList:
##                            INFILES.append(OUTFILE)
##                    for infile in INFILES:
##                        shutil.copy2(ExpFileLocation+ "\\" + infile, modelDirectory)

                # move in files
                if trial > 0:
                    directory = srcDrive+"ProgrammingFolder\\HYDRUS_Data\\Projects\\Results\\"+exp+"\\Ensemble\\Simulation "+str(model)+"\\Trials\\Trial= "+str(trial-1)

                    pkl_file = open('C:\\Derek\\CropModel\\lAssim.pkl', 'rb')
                    lAssim = pickle.load(pkl_file)
                    pkl_file.close()

                    moveEnsembleFiles(ExpFileLocation,directory)

                    if lAssim:                        
                        tempDir = srcDrive+"ProgrammingFolder\\HYDRUS_Data\\Projects\\Results\\"+exp+"\\Ensemble\\Simulation "+str(0)+"\\Trials\\Trial= "+str(trial-1)
                        pkl_file = open(tempDir+'\\xPostList.pkl', 'rb')
                        xPostList = pickle.load(pkl_file)
                        pkl_file.close()
                        xPostList = np.array(xPostList)
                        info = xPostList[trial-1,:,model]
                    else:
                        info = []

                    updateEnsembleIN(ExpFileLocation,numLayers,data = info,trial=model,update=lAssim)


##                    updateAssimIN(ExpFileLocation)

                paramDict = {'TPrint(1),TPrint(2),...,TPrint(MPL)':np.arange(trial+1)+1,
                             'tMax':trial+1,'tInit':trial,'MPL':trial+1,'Trial':trial}
                setSelectorParams(ExpFileLocation,paramDict)
                    
                print("Start of Trial ",trial,'... ')
                hydrus.run_hydrus(noCMDWindow,str(1))
                fileLocation = hydrus.outputResults("Ensemble\\Simulation "+str(model)+"\\Trials",str(trial))

            # Calculate co-variances
            directory = srcDrive+"ProgrammingFolder\\HYDRUS_Data\\Projects\\Results\\"+exp+"\\Ensemble\\Simulation 0\\Trials\\Trial= 0"
            dirResults = srcDrive+"ProgrammingFolder\\HYDRUS_Data\\Projects\\Results\\"+exp+"\\Ensemble\\"
            if trial < numDays-1:
                calculateVariances(directory,numModels,trial,dirResults)

        print('Done...')

    stopTime = time.clock()
    lengthOfRun = stopTime - startTime
    timeOfDay = time.localtime(time.time())
    print('Took:   '+str(lengthOfRun)+' seconds,  Finished at:  '+str(timeOfDay[3])+':'+str(timeOfDay[4]))


def setDataIN(ExpFileLocation,paramDict,label='*ASSIMILATION'):

    dataIN = DATAIN(ExpFileLocation)

    for param in paramDict.keys():
        dataIN.setData(param,paramDict[param],heading=label)

    dataIN.update()

def getAllTexParams(prct='two', model='old', perturb_prct=None):

    srcDrive = "C:\\Derek\\"
    directory = srcDrive+"ProgrammingFolder\\Projects\\Clustering\\simpleSoilClustering\\"

    water = WC()
    paramValues = water.getParams(prct,model)

    if perturb_prct != None:
        dataDict = loadmat(directory+'WC_SW605_perturbed'+str(perturb_prct)+'_params_oldold.mat')
        paramValues = dataDict['params'][:]
    
    return paramValues

def getAllSSC(prct='two',model='old'):

    water = WC()
    SSCData = water.getSSC(prct,model) 

    return SSCData

def getSoilParams(ExpFileLocation):
    paramList = ['thr','ths','Alfa','n','Ks','l']

    incrementList = [1.0,0.95,0.90,1.05,1.10]
##    incrementList = [1.0]
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

def updateProfileDAT(ExpFileLocation,numLayers):
    nodInf = NODINF(ExpFileLocation)
    profile = PROFILEDAT(ExpFileLocation)
    data = nodInf.getHeadData('end')

    for i in range(1,len(data)):
        temp = format(data[i],'.6e')
        if len(temp.split('e')[1]) < 4:
            temp = temp.split('e')[0]+'e+0'+temp.split('e')[1][1:]
        profile.setData('h',temp,layer=i-1)


def setSelectorParams(ExpFileLocation,paramDict,nmat = 1):

    selectorIN = SELECTORIN(ExpFileLocation)

    for param in paramDict.keys():
        selectorIN.setData(param,paramDict[param],mat = nmat)

    selectorIN.update()


def calculateVariances(initialDirectory,numModels,trial,resultsDirectory):


    Sim0Dir = resultsDirectory + "Simulation "+str(0)+"\\Trials\\Trial= "+str(trial)

##    print ExpFileLocation

    obsDOY = -99

    dataIN = DATAIN(Sim0Dir)
    
    numLayers = int(dataIN.getData('NL'))
    N = 1
    M = int(dataIN.getData('M'))  # number of observations

    
##    N = int(dataIN.getData('N'))  # number of time steps in assim
    
##    Q = dataIN.getData('Q')
##    R = dataIN.getData('R')

##    os.chdir('C:\\Derek\\CropModel\\')

##    pkl_file = open('C:\\Derek\\CropModel\\covR_random.pkl', 'rb')
    pkl_file = open('C:\\Derek\\CropModel\\covR_obs.pkl', 'rb')
    R = pickle.load(pkl_file)
    pkl_file.close()

##    print R * 10.0

    R = R[:M,:M] # * 100.0
##    print R.shape

##    R = np.array([temp[0,0]])  # related to the number of observations

    xf = np.zeros((numLayers,numModels))

##    ## for CropModel
##    temp = 'C:\\Derek\\ProgrammingFolder\\HYDRUS_Data\\Projects\\CropModel\\'
##    assimData = ASSIMDATA(temp)
##    
##    try:
##        ## for CropModel
##        y = assimData.getData(str(trial))
##        y = np.array([y]*numModels)
##
##        obsDOY = trial
##    except UnboundLocalError:
##        print ' UnboundLocalError...'
##        pass

##    obsDOY = trial + 1 #


        
    dataout = DATAOUT(Sim0Dir)
    t = float(dataout.getData('t'))


##    dataIN = ENSEMBLEOUT(ExpFileLocation)
##    numLayers = dataIN.getData('NL')
##    ensOut = ENSEMBLEOUT(folder+'ENSEMBLE.OUT')
##    H = np.array(ensOut.getData('H'))
    
    I = np.eye(N)
    H = np.ones((M,N))

    if trial > 0:
        pkl_file = open(Sim0Dir+'\\Paposteriori.pkl', 'rb')
        P = pickle.load(pkl_file)
        pkl_file.close()
        papriori = np.array(P[-1])

        pkl_file = open(Sim0Dir+'\\KList.pkl', 'rb')
        KList = pickle.load(pkl_file)
        pkl_file.close()
        
        pkl_file = open(Sim0Dir+'\\xPostList.pkl', 'rb')
        xPostList = pickle.load(pkl_file)
        pkl_file.close()

        pkl_file = open('C:\\Derek\\CropModel\\obsList.pkl', 'rb')
        obsList = pickle.load(pkl_file)
        pkl_file.close()

        if len(obsList) > 0:
            obsDOY = obsList[0]
        else:
            obsDOY = -99

        if trial + 1 == obsDOY:
            obsList = obsList[1:]

        output = open('C:\\Derek\\CropModel\\obsList.pkl','wb')
        pickle.dump(obsList, output)
        output.close()

    else:
        KList = []
        xPostList = []
        P = []
        papriori = np.zeros((numLayers,numModels))

        obsList = np.arange(2,182)  # Everyday
##        obsList = np.arange(5,175,5) # 5 Days
        obsList = np.arange(6,181,14) # 14 Days
##        obsList = []
        output = open('C:\\Derek\\CropModel\\obsList.pkl','wb')
        pickle.dump(obsList, output)
        output.close()

    paposteriori = np.zeros((numLayers,numModels))
    xpostLayers = np.zeros((numLayers,numModels))

    lAssim = False

    print(obsDOY)
    if np.abs(obsDOY - t) <= 0.000001:
        y = np.zeros((M,numLayers))
        lAssim = True
        for obsLocation in range(M):
            soil = 14  # 14=712(clay loam,base)
    ##        ExpFileLocation = resultsDirectory + "Simulation "+str(model)+"\\Trials\\Trial= "+str(trial)
    ##        assimData = ASSIMDATA(ExpFileLocation,'assimdata'+str(model)+'.txt')
            assimData = ASSIMDATA('C:\\Derek\\CropModel\\','assimdata'+str(soil)+'.txt')
            y[obsLocation,:] = assimData.getData(str(obsDOY))
        
        for model in range(numModels):
            ExpFileLocation = resultsDirectory + "Simulation "+str(model)+"\\Trials\\Trial= "+str(trial)

            nodInf = NODINF(ExpFileLocation)
            data = nodInf.getWCData('end',stopLine=numLayers)

            xf[:,model] = data

##            R = ensOut.getData('R')
##        for layer in range(numLayers):
##            xbar = np.mean(xf[:,layer])
##            # papriori should be a NxN matrix I think. Does np.sum do this?
##            papriori = (1.0/(numModels-1.0))*(np.sum(dot((xf[:,layer]-xbar),(xf[:,layer].T-xbar))))
##            K = dot(dot(papriori,H.T),(dot(dot(H,papriori),H.T)+R)**(-1))
##            paposteriori = dot((I-dot(K,H)),papriori)
##            xaposteriori = np.mean(xf[:,layer] + dot(K,(y[layer]-dot(H,xf[:,layer]))))
##            layerData[layer,:] = [xbar,papriori,K,paposteriori,xaposteriori]
##        layerData = np.zeros((numLayers,2))
##            ##        temp = np.zeros((numLayers))
##        product = np.zeros((numLayers,numModels))
##
####        for i in range(numModels):
####            product[:,i] = np.dot((xf[:,i]-xbar),(xf[:,i]-xbar).T)
####        np.subtract(xf[:,:],np.array(xbar))
##        product[:,:] = np.dot(np.subtract(xf[:,:],xbar),np.subtract(xf[:,:],xbar).T)
##        
####        for i in range(numLayers):
####            temp[i] = np.sum(product[i,:])

        
        xbarLayers = np.zeros((numLayers))

        
        Karray = np.zeros((numModels,numLayers,M))

        for layer in range(numLayers):
            xaposteriori = np.zeros((numModels))
            xbar = np.mean(xf[layer,:])
            for model in range(numModels):
                product = np.dot(np.subtract(xf[layer,model],xbar),np.subtract(xf[layer,model],xbar).T)
                papriori = (1.0/(numModels-1.0))*product
##                print papriori,xbar
##            print papriori.shape,H.T.shape,R.shape

                K = np.dot(np.dot(papriori,H.T),(np.dot(np.dot(H,papriori),H.T)+R)**(-1))
##                K = (np.dot(papriori,H.T))*((np.dot(np.dot(H,papriori),H.T)+R)**(-1))
##                print K
                paposteriori[layer,model] = np.dot((I-np.dot(K,H)),papriori)
##                print 'dot(K,H)',np.dot(K,H)
##                print K,paposteriori[layer,model]
                
                Karray[model,layer,:] = K
##                obs = np.zeros((M,1))
##                obs[:,0] = y[:,layer]

##            print K.shape,obs.shape,np.dot(H,xf[layer,model]).shape,xf[layer,model].shape

##            for model in range(numModels):
                
##                print obs,xf[layer,model]
##                adjust = obs-np.dot(H,xf[layer,model])
##                print 'adjust',np.dot(K,(obs-np.dot(H,xf[layer,model])))
                temp = xf[layer,model] + np.dot(K,(y[:,layer]-np.dot(H,xf[layer,model])))
##                print temp.shape,xf[layer,model].shape
##                print temp
                xaposteriori[model] = temp

##                print xaposteriori[model]
##            print xaposteriori
            xpostLayers[layer,:] = xaposteriori
            xbarLayers[layer] = xbar
            
##        if t > 13:
##            print trial
##            print xf
##            print xaposteriori
               
##        layerData = [xbarLayers,xpostLayers]

        
    else:
        print('not updating')
        print(obsDOY,t)
        Karray = np.zeros((numModels,numLayers,M))
        for layer in range(numLayers):
            for model in range(numModels):
                K = np.dot(np.dot(papriori[layer,model],H.T),(np.dot(np.dot(H,papriori[layer,model]),H.T)+R)**(-1))
                paposteriori[layer,model] = np.dot((I-np.dot(K,H)),papriori[layer,model])
                Karray[model,layer,:] = K

        
    P.append(paposteriori)

    output = open(Sim0Dir+'\\Paposteriori.pkl','wb')
    pickle.dump(P, output)
    output.close()

    KList.append(Karray)

    output = open(Sim0Dir+'\\KList.pkl','wb')
    pickle.dump(KList, output)
    output.close()

    xPostList.append(xpostLayers)
    
    output = open(Sim0Dir+'\\xPostList.pkl','wb')
    pickle.dump(xPostList, output)
    output.close()
    
    output = open('C:\\Derek\\CropModel\\'+'lAssim.pkl','wb')
    pickle.dump(lAssim, output)
    output.close()

##    for model in range(numModels):
##        ## directory = results location
##        ExpFileLocation = resultsDirectory + "Simulation "+str(model)+"\\Trials\\Trial= "+str(trial)
####        print ExpFileLocation
##        infile = open(ExpFileLocation+'\\ASSIM.IN','r')
##        lines = infile.readlines()
##        infile.close()
##
##        outfile = open(ExpFileLocation+'\\ASSIM.IN','w')
##        outfile.writelines(lines[:8])

##    paramList = ['Q','R','A','H','xapriori','residual']
##    paramList = ['R','H','xapriori','residual']
##
##    for param in paramList:
##        data = ensOut.getData(param)
##        outfile.write('*'+param+'\n')
##        writeLines = [line.join(',')+'\n' for line in data]
##        outfile.writelines(writeLines)
##        outfile.write('\n')
##        outfile.write('\n')

##        if (obsDOY - t) <= 0.000001:
##
##            paramList = ['xaposteriori']
##            paramData = [xpostLayers[:,model]]  # K[numLayers,numModels], papo[numLayers], xpost[numLayers,numModels]
##            
##            # write new analysis value to ASSIM.IN
##            #  - if EnKF have HYDRUS overwrite new value after assimilation
##
##            for i in range(len(paramList)):
##                writeLines = []
##                outfile.write('*'+paramList[i]+'\n')
####                writeLines = [str(paramData[i][j]).join(',')+'\n' for j in range(len(paramData[i]))]
##                [writeLines.append(str(paramData[i][j])+'\n') for j in range(len(paramData[i]))]
##                outfile.writelines(writeLines)
##                outfile.write('\n')
##                outfile.write('\n')
##            
##            outfile.close()


def setAtmosh(ExpFileLocation,prec,tatm):

    atmoshIN = ATMOSPHIN(ExpFileLocation)

    # atmoshIN.setData('MaxAL',numDays)
    # atmoshIN.setData('hCritS',5)
    
    offset = 0
##    steps = [0.7,0.8,0.9]
##    precs = [0.2,0.4,0.6]
##    steps = [2.0,1.0]
##    precs = [0.25,0.5]
    # steps = [1.0]
    # precs = [0.5]

    atmoshIN.setData('Prec',prec,1+offset)
            
    atmoshIN.setData('hCritA',10000,1+offset)

    atmoshIN.setData('tAtm',tatm,1+offset)

    atmoshIN.update()

def setMeteo(srcDrive,ExpFileLocation,filename,numDays,iRadiation=2,iCrop=0,year='04',albedo=0.15):
##    Ensemble Mode 6
    infile = open(filename,'r')
    lines = infile.readlines()
    infile.close()

    lat = float(lines[2].split()[1])
    alt = float(lines[2].split()[3])

    info = np.zeros((numDays,7))
    if year == '04':
        offset = 0
##        offset = 8  # offset used before using days to planting, dtp, variable
    else:
        offset = 384 # offset used before using days to planting, dtp, variable
        
    for i in range(numDays):
        info[i,1:] = [float(item) for item in lines[i+4+offset].split()[1:]]
        info[i,0]  = int(lines[i+4+offset].split()[0][2:])
        
    meteoIN  = METEOIN(ExpFileLocation)
    atmoshIN = ATMOSPHIN(ExpFileLocation)

    for infile in [meteoIN,atmoshIN]:
        if numDays < infile.getNumTimes():
            infile.delLines(numDays)
        elif numDays > infile.getNumTimes():
            infile.addLines(numDays)

    # 0: HYDRUS Calc. RAD, 2: RAD given; must be first
    if iRadiation == 0: filename = srcDrive+'ProgrammingFolder\\CropModel\\Meteo_iRad0.dat'
    elif iRadiation == 2: filename = srcDrive+'ProgrammingFolder\\CropModel\\Meteo_iRad2.dat'
    meteoIN.setData('Radiation',iRadiation,fname=filename)
    if iCrop == 0:
        meteoIN.delInterception(iRadiation,albedo,iCrop)
    meteoIN.setData('iCrop',iCrop)
    meteoIN.setData('Latitude',lat)
    meteoIN.setData('Altitude',alt)
    meteoIN.setData('MeteoRecords',numDays)
    meteoIN.addData()
    for i in range(numDays):
        meteoIN.setData('Rad',info[i,1],i)
        meteoIN.setData('TMax',info[i,2],i)
        meteoIN.setData('TMin',info[i,3],i)
        meteoIN.setData('RHMean',info[i,5],i)
        meteoIN.setData('Wind',info[i,6],i)
##        if iCrop == 3:
##        meteoIN.setData('rRoot','0',i)
##        meteoIN.setData('LAI(SCF)','0',i)
##        meteoIN.setData('Albedo','0.23',i)
##        meteoIN.setData('CropHeight','0',i)
        meteoIN.setData('DOY',info[i,0],i)
##        Not needed but will, remove the data in these columns if removed in decreasing order
##        meteoIN.setData('DOY',' ',i)
##        meteoIN.setData('rRoot',' ',i)
##        meteoIN.setData('LAI(SCF)',' ',i)
##        meteoIN.setData('Albedo',' ',i)
##        meteoIN.setData('CropHeight',' ',i)
        
    atmoshIN.setData('MaxAL',numDays)
    atmoshIN.setData('hCritS',5)
    
    offset = 0
##    steps = [0.7,0.8,0.9]
##    precs = [0.2,0.4,0.6]
##    steps = [2.0,1.0]
##    precs = [0.25,0.5]
    steps = [1.0]
    precs = [0.5]

    for i in range(numDays):
        ind = i
        if float(info[i,4]) > 5.0:
##            atmoshIN.insertData(ind+1+offset,[ind+1-step for step in steps])
            for j in range(len(precs)):
                atmoshIN.setData('Prec',precs[j],ind+j+offset-1)
##            offset += len(precs)
            print(ind,ind+offset,precs[j])
            atmoshIN.setData('Prec',(info[i,4])/10.0-precs[0],ind+offset)
##        if float(info[i,4]) > 75.0:
##            atmoshIN.setData('Prec',(info[i,4]/10.0),ind+offset)
        else:
            atmoshIN.setData('Prec',info[i,4]/10.0,ind+offset)
            
##        atmoshIN.setData('Prec',info[i,4]/10.0,ind+offset)
        atmoshIN.setData('hCritA',100000,ind+offset)

    atmoshIN.update()
    meteoIN.update()
    

def moveEnsembleFiles(ExpFileLocation,directory):
    INFILES = [] 
    os.chdir(directory)
    currentDir = os.curdir
    dirList = os.listdir(currentDir)
                            
    #moves all the files to a directory
    for infile in dirList:
        shutil.copy2(directory+ "\\" + infile, ExpFileLocation)    


def updateAssimIN(ExpFileLocation):
    # update EnKF input file
    infile = open(ExpFileLocation+'\\ASSIM.OUT','r')
    lines = infile.readlines()
    infile.close()

    outLines = lines

    infile = open(ExpFileLocation+'\\ASSIM.IN','r')
    lines = infile.readlines()
    infile.close()
    
    outfile = open(ExpFileLocation+'\\ASSIM.IN','w')
    outfile.writelines(lines[:5])
    outfile.writelines(outLines)
    outfile.close()  


def updateEnsembleIN(ExpFileLocation,numLayers,data=[],trial=0,update=False):
    # update ensemble input file
    infile = open(ExpFileLocation+'\\DATA.OUT','r')
    lines = infile.readlines()
    infile.close()
    
##  Used for non-ensemble updating....
    outfile = open(ExpFileLocation+'\\ENSEMBLE.IN','w')
    offset = 0
    if trial == 1:
        offset = 0
    outfile.writelines(lines[offset:18+offset])
    outfile.writelines(lines[67+numLayers+18+3+offset:67+numLayers+18+5+offset])
    outfile.writelines(lines[20+offset:67+numLayers+3+offset])
    outfile.close()


##    shutil.copy2(ExpFileLocation+'\\ENSEMBLE.IN', 'C:\\Derek\\CropModel\\\\ENSEMBLE'+str(trial)+'.IN')

    if update:
        infile = open(ExpFileLocation+'\\ENSEMBLE.IN','r')
        lines = infile.readlines()
        infile.close()

        outfile = open(ExpFileLocation+'\\ENSEMBLE.IN','w')
        outfile.writelines(lines[:70+(numLayers-len(data))])

    ##    print len(data)

        for i in range(len(data)):
            ind = (70 + numLayers - len(data)) + i
            line = lines[ind].split()
            line[8] = str(data[-(i+1)])
            line[9] = str(data[-(i+1)])
    ##        line[8] = str(0.000)
            wline = ' '
            for item in line:
                wline += item +' '
            wline += '\n'
            outfile.writelines(wline)

        outfile.close()


def main():
    runCropModel()
             
if __name__ == "__main__":
    main()
       

        
