#HYDRUS_Class.py
#Created by Derek Groenendyk
#10/16/2011
#Class that runs HYDRUS, modifies the input files, and arranges the output data.

#import tkSimpleDialog
#import tkFileDialog
# from tkinter import *
# from tkinter import *
## import messageBox
import shutil
import os
import types
from win32com.client import *
import subprocess
import sys
import shlex
# import pandas as pd 
import numpy as np
from scipy.io import *
import pickle as pkl

from hydrus.outfiles import *
import time
from scipy.io import FortranFile


class HYDRUS:
    
    def __init__(self,ExpFileLocation,exp):
        self.directory = ExpFileLocation
        self.exp = exp
        # list of file extensions of interest
        self.fileExtList = [".out",".in",".txt",".dat",".pkl"]

    #runs the HYDRUS program    
    def run_hydrus(self,noCMDWindow):
        args = r'C:\HYDRUS-1D 4.xx\cropmodel.exe'
##        args = r'C:\HYDRUS-1D 4.xx\H1D_CALC.exe'
##        args = r"H1D_CALC"
##        temp = args + ' ' + self.directory
##        print str.replace(temp,'\\','/')
##        command_line = args + ' ' + self.directory
##        args2 = shlex.split(command_line)
        args2 = [args,self.directory]
        args += ' ' + self.directory

##        print args2
        
        # if subprocess.mswindows:
        #     su = subprocess.STARTUPINFO()
            
        #     if noCMDWindow == 1:
        #         su.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        #         su.wShowWindow = subprocess.SW_HIDE 
        #     else:
        #         su.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        #         su.wShowWindow = 1 #SW_SHOW = 5,  SW_SHOWNORMAL = 1

##        try:
##            retcode = subprocess.call(args,shell=True,startupinfo=su)
##            if retcode < 0:
##                print >>sys.stderr, "Child was terminated by signal", -retcode ," Trial ", trial
##            else:
##                print >>sys.stderr, "Child returned", retcode ," Trial ", trial
##        except OSError, e:
##            print >>sys.stderr, "Execution failed:", e," Trial ", trial

                
########## last use 9.1.2015 DGG  ######################################################################################            
#         try:
# ##            process = subprocess.call(args,startupinfo=su)
# ##            print 'calling'
#             p = subprocess.Popen(args2,shell=True,startupinfo=su,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
# ##            print 'called'
# ##            p = subprocess.Popen(args2,startupinfo=su)
# ##            (child_stdout,child_stderr) = (p.stdout, p.stderr)
# ##            p.stdin.close()
#             (stdoutData, stderrData) = p.communicate()
#             print(stdoutData)
#             print(stderrData)
#         except:
#             pass
########################################################################################################################


        try:
            out = subprocess.check_output(args2, shell=False,stderr=subprocess.STDOUT)
            if noCMDWindow != 1:
                print(out.decode("utf-8"))
        except subprocess.CalledProcessError as e:
            print(e.output)




            
##            if p.wait() != 0:
##                print "There were some errors"
##            for line in child_stdout:
##                print line
##            for line in child_stderr:
##                print line
##        except subprocess.CalledProcessError, e:
##            print e.cmd
##            print e.returncode
##            print "HYDRUS stdout output:\n", e.output

##            process = subprocess.check_output(args2,shell=True,startupinfo=su)
##        except subprocess.CalledProcessError, e:
##            print e.cmd
##            print e.returncode
##            print "HYDRUS stdout output:\n", e.output

##            process = subprocess.call(args,startupinfo=su)
##        except subprocess.CalledProcessError, e:
##            print e.cmd
##            print e.returncode
##            print "HYDRUS stdout output:\n", e.output

##            process = subprocess.Popen(args2,startupinfo=su,stdin=subprocess.PIPE,
##                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
##            process.stdin.close()
##            if process.wait() != 0:
##                print "There were some errors"
            
##            process = subprocess.check_call(args2,startupinfo=su)
##            output = subprocess.check_output(['ls', '-lt'])
##            print output
            
##            process = subprocess.check_output(args,stderr=subprocess.STDOUT)
##            print process.stderr.readline()
##            print process.stdout.readline()
##            print process.returncode
##            retcode = subprocess.call(args,startupinfo=su)
##            if retcode < 0:
##                print >>sys.stderr, "Child was terminated by signal", -retcode ," Trial ", trial
##            else:
##                print >>sys.stderr, "Child returned", retcode ," Trial ", trial
##        except OSError, e:
##            print >>sys.stderr, "Execution failed:", e," Trial ", trial

    # modifies the HYDRUS LEVEL_01.DIR file
    # not needed if you provide the experiment location to HYDRUS
    def update_LEVEL01(self,newExpFileLocation = None):
        if newExpFileLocation == None:
            newExpFileLocation = self.directory
        
        hydrusDirectory = "C:\\HYDRUS-1D 4.xx"
        try:
            infile = open(hydrusDirectory+"\\LEVEL_01.DIR","r+")
        except IOError:
            root = Tk()
            root.withdraw()
            createLEVEL01 = tkMessageBox.askyesno("Warning!","LEVEL_01.DIR file does not exist!! Would you like to create it now?")
            if createLEVEL01:
                infile = open(hydrusDirectory+"\\LEVEL_01.DIR","w")
            else:
                exit()
        
        
        infile.write(newExpFileLocation)
        infile.close()

    #moves the output files and creates output folders
    def outputResults(self,parameter,trial):
        
        INFILES = []
        
        os.chdir(self.directory)
        self.currentDir = os.curdir
        self.dirList = os.listdir(self.currentDir)
        
        #adds all the files of interest to INFILES
        for OUTFILE in self.dirList:
            if os.path.splitext(OUTFILE)[1].lower() in self.fileExtList:
                INFILES.append(OUTFILE)
                
        
        #gets information about the assimilation to create the right folders/files

        directory = "C:\\Derek\\ProgrammingFolder\\HYDRUS_Data\\Projects\\Results\\"+self.exp
        
        resultsDir = directory +"\\"+parameter+"\\Trial= "+trial 
        
        #informs user if folders already exist, and asks if they should be overwritten.
        try:
            os.makedirs(resultsDir)
        except OSError:
            while True:
                try:
                    shutil.rmtree(resultsDir)
                except WindowsError:
                    time.sleep(10)
                else:
                    os.makedirs(resultsDir)
                    break


##            root = Tk()
##            root.withdraw()
##            writeResults = tkMessageBox.askyesno("Warning!","Results directory already exists. Would you like to overwrite?")
##            if writeResults:
##                shutil.rmtree(resultsDir)
##                os.makedirs(resultsDir)
##            else:
##                exit()

        #moves all the files to a directory
        for infile in INFILES:
##            print infile
            shutil.copy2(self.directory+ "\\" + infile, resultsDir)
##            shutil.move(self.directory+ "\\" + infile,resultsDir)

        return resultsDir

    def saveOutput(self,ind,expType,depth,db=None,numtrials=None,trial=None):

        # exp = 'simpleClusterPerturbed'

        srcDrive = 'C:\\Derek\\'
        # dataDir = srcDrive+'ProgrammingFolder\\Projects\\simpleSoilClustering\\PerturbedData\\Trial '+str(ind)+'\\'
        
        resultsDir = srcDrive+'ProgrammingFolder\\HYDRUS_Data\\Projects\\Results\\'

        # try:
        #     os.makedirs(dataDir)
        # except OSError:
        #     shutil.rmtree(dataDir)
        #     os.makedirs(dataDir)

        days = range(202)
        if expType in ['SW605_InfOnly','SW605','SW605_FreeDrainage']:
            if expType == 'SW605_InfOnly':
                days = range(42)
            if expType == 'SW605_FreeDrainage':
                days = range(162)

        numTrials = 1326
        
        if trial != None:
            dataDir = srcDrive+'ProgrammingFolder\\Projects\\Clustering\\simpleSoilClustering\\ChunkedData\\'
            WCData = np.zeros((len(days),depth))
            # dataDict = {'wc': WCData}
            # if trial == 0:
            #     WCData = np.zeros((numtrials,len(days),depth))
            # else:
            #     dataDict = loadmat(self.directory+'\\'+expType+'_wcdata.mat')
            #     WCData = dataDict['WC_Data']['wc'][0][0]
                # print(WCData)

             # list of average wc over depth for each trial for each day

            #Initialize Classes
            nodInf = NODINF(self.directory,lbinary=False)
            for day in days:
                if day > len(nodInf.getTimes())-1:
                    wc = np.array([0.0])
                else:
                    wc = nodInf.getWCData(day,depth)
                # print(wc.shape)
                # print(WCData.shape)
                WCData[day,:] = wc*1.0

            dataDict = {'wc': WCData}
            # savemat(self.directory+'\\'+expType+'_wcdata.mat', mdict={'WC_Data':dataDict},do_compression=True)
            savemat(dataDir+expType+'\\'+db+'\\'+'Trial'+str(trial)+'.mat', mdict={'WC_Data':dataDict},do_compression=True)

        # numTrials = 15
        # wcList = []

        # if ind == 0 and trial == 0:
            # WCData = np.zeros((1000,numTrials,len(days),depth))
            # dataDict = {'wc': WCData}
            # savemat(dataDir+db+'.mat', mdict={'WC_Data':dataDict},do_compression=True)       
            
        else:
            dataDir = srcDrive+'ProgrammingFolder\\Projects\\Clustering\\simpleSoilClustering\\PerturbedData\\'
            WCData = np.zeros((numTrials,len(days),depth)) # list of average wc over depth for each trial for each day
            for trial in range(numTrials):
                if db != None:
                    ResultsFileLocation = resultsDir+expType+'\\'+db+'\\Trial= '+str(trial)
                elif exp == 'simpleCluster':
                    ResultsFileLocation = resultsDir+expType+'\\ROSETTA - 2 Percent\\Trial= '+str(trial)
                elif exp == 'simpleClusterPerturbed':
                    ResultsFileLocation = resultsDir+expType+'\\ROSETTA - 2 Percent - perturbed1000\\Trial= '+str(trial)
                elif exp == 'CropModel':
                    ResultsFileLocation = resultsDir+'CropModel\\'+expType+'\\Trial= '+str(trial)

                #Initialize Classes
                nodInf = NODINF(ResultsFileLocation,lbinary=True)
                for day in days:
                    if day > len(nodInf.getTimes())-1:
                        wc = np.array([0.0])
                    else:
                        wc = nodInf.getWCData(day,depth)
        ##            WCData[trial,ind] = wc.mean()*depth*1.0
                    # if trial == 7:
                        # print(wc[0],WCData.shape)
                    WCData[trial,day,:] = wc*1.0

            # pkl_file = open(dataDir+'data'+str(ind)+'.pkl', 'wb')
            # pkl.dump(WCData, pkl_file)
            # pkl_file.close()

            dataDict = {'wc': WCData}
            savemat(dataDir+'data'+str(ind)+'.mat', mdict={'WC_Data':dataDict},do_compression=True)
                
                # if not os.path.exists(dataDir+db+'.mat'):

                # dataDict = loadmat(dataDir+db+'.mat')
                # data = dataDict['WC_Data']['wc'][0,0][:]
                # data = np.append(data,[WCData],axis=0)
                # dataDict = {'wc': WCData}

                # dataDict = {'wc': WCData}
                # savemat(dataDir+db+'.mat', mdict={'WC_Data':dataDict},do_compression=True)










