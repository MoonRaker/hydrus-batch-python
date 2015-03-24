#HYDRUS_Class.py
#Created by Derek Groenendyk
#10/16/2011
#Class that runs HYDRUS, modifies the input files, and arranges the output data.

#import tkSimpleDialog
#import tkFileDialog
from Tkinter import *
import tkMessageBox
import shutil
import os
import types
from win32com.client import *
import subprocess
import sys
import shlex

class HYDRUS:
    
    def __init__(self,ExpFileLocation,exp):
        self.directory = ExpFileLocation
        self.exp = exp
        # list of file extensions of interest
        self.fileExtList = [".out",".in",".txt",".dat",".pkl"]

    #runs the HYDRUS program    
    def run_hydrus(self,noCMDWindow,trial):
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
        
        if subprocess.mswindows:
            su = subprocess.STARTUPINFO()
            
            if noCMDWindow == 1:
                su.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                su.wShowWindow = subprocess.SW_HIDE 
            else:
                su.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                su.wShowWindow = 1 #SW_SHOW = 5,  SW_SHOWNORMAL = 1

##        try:
##            retcode = subprocess.call(args,shell=True,startupinfo=su)
##            if retcode < 0:
##                print >>sys.stderr, "Child was terminated by signal", -retcode ," Trial ", trial
##            else:
##                print >>sys.stderr, "Child returned", retcode ," Trial ", trial
##        except OSError, e:
##            print >>sys.stderr, "Execution failed:", e," Trial ", trial

                
            
        try:
##            process = subprocess.call(args,startupinfo=su)
##            print 'calling'
            p = subprocess.Popen(args2,shell=True,startupinfo=su,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
##            print 'called'
##            p = subprocess.Popen(args2,startupinfo=su)
##            (child_stdout,child_stderr) = (p.stdout, p.stderr)
##            p.stdin.close()
            (stdoutData, stderrData) = p.communicate()
            print stdoutData
            print stderrData
        except:
            pass




            
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
            shutil.rmtree(resultsDir)
            os.makedirs(resultsDir)
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
