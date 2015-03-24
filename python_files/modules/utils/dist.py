#import tkSimpleDialog
#import tkFileDialog
from Tkinter import *
import tkMessageBox
import shutil
import os
import types
#import win32gui
#win32gui.MessageBox(0, "Directory already exist! No data overwritten", "Warning!", 1)
from win32com.client import *
import scipy.stats as st 
import matplotlib as mp
import scipy as sp
import matplotlib.pyplot as plt
from random import randrange
from math import sqrt
import numpy as np

class Stats:
    
    def __init__(self,data,param='None'):
        self.directory = os.getcwd()
        self.currentDir = os.curdir
        self.dirList = os.listdir(self.currentDir)
        self.name = param
        if param == "SKSS":
            self.index = 0
        elif param == "SSAT":
            self.index = 1
        elif param == "SDUL":
            self.index = 2
        elif param == "SLLL":
            self.index = 3

        self.X = data
        self.updateStats()

    def normalityPlot(self):
        fig1 = plt.figure()  # set up plot
        ax = fig1.add_subplot(1, 1, 1)
    
        ax.plot(self.osm, self.osr, '.', self.osmf, self.osrf, 'b-')
        ax.set_title('Normailty Plot')

    def rankPlot(self):
        fig2 = plt.figure()
        ax = fig2.add_subplot(1, 1, 1)
        
        ax.plot(self.Z,sp.sort(self.X),'*',self.x,self.y,'-')
        ax.set_title('Rank Plot')

    def histogramPlot(self,name,numBins=100,lines=[]):
        fig3 = plt.figure()
        ax = fig3.add_subplot(1, 1, 1)

        print self.X
        
        # the histogram of the data
        n, bins, patches = plt.hist(self.X, numBins, normed=1, facecolor='green', alpha=0.75)

        # add a 'best fit' line
        bincenters = 0.5*(bins[1:]+bins[:-1])
        y = mp.mlab.normpdf(bincenters, self.mean, self.sd)
        l = ax.plot(bincenters, y, 'r--', linewidth=1)
        print np.sum(n * np.diff(bins))

        limits = ax.axis()

        if lines != []:
            for i in range(len(lines)):
                ax.plot([lines[i][0],lines[i][0]],[0,round(limits[3],4)],linewidth=2,color='b')
                ax.plot([lines[i][1],lines[i][1]],[0,round(limits[3],4)],linewidth=2,color='b')
                x = lines[i][0] + 0.5*(lines[i][1]-lines[i][0])
                ax.text(x,limits[3]/2.0,str(i+1))

        

        ax.set_xlabel(self.name)
        ax.set_ylabel('Frequency')
        #ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
        ax.set_title('Histogram')
        #plt.axis([40, 160, 0, 0.03])
        ax.grid(True)
##        plt.show()
        self.saveFig(fig3,name,'png')
        
    def saveFig(self,fig,filename,ext,DPI=300):
        fig.savefig('C:\\Temp\\Pics\\'+filename+'.'+ext,format = ext,dpi = DPI)            

    def write(self,fileName,run,power,wType='append'):
        if os.path.exists(self.directory+"\\"+fileName+'.txt'):
            if wType != 'append':
                outfile = open(self.directory+"\\"+fileName+'.txt',"w")
            else:
                infile = open(self.directory+"\\"+fileName+'.txt','r')
                LineData = infile.readlines()
                infile.close()
                outfile = open(self.directory+"\\"+fileName+'.txt',"w")
                outfile.writelines(LineData)
        else:
            outfile = open(self.directory+"\\"+fileName+'.txt',"w")
            
        outfile.write('Trt '+run+' Stats -  size= '+str(len(self.X))+', power= '+str(power)+'\n')
        outfile.write(' mean=%.3f stdev=%.3f \n'%(self.mean,self.sd))
        outfile.write(' ratio=%.3f diff1=%.3f diff3= %.3f\n'%(self.ratio,self.diff1,self.diff3))  #for normality should be ~1.34
        outfile.write(' kutosis=%.3f p-value=%.3f\n'%(self.k,self.ktrue[1]/2))    #1-sided p-value, ~3
        outfile.write(' skewness=%.3f p-value=%.3f\n'%(self.s,self.strue[0]/2))   #1-sided p-value, ~0
        outfile.write(' CV=%.3f CI=[%.3f,%.3f] @ 95\n'%(self.CV,self.CI[0],self.CI[1]))
        #Coefficient of Variation calculations, CV
        # 1.96 indicates 95% significance level

        outfile.write(' anderson=%.3f 10=%.3f 5=%.3f 2.5=%.3f 1=%.3f (entire distribution)\n'%(self.andy[0],self.andy[1][1],self.andy[1][2],self.andy[1][3],self.andy[1][4]))
        outfile.write(' anderson=%.3f 10=%.3f 5=%.3f 2.5=%.3f 1=%.3f (0.10 sample)\n'%(self.sampleAndy[0],self.sampleAndy[1][1],self.sampleAndy[1][2],self.sampleAndy[1][3],self.sampleAndy[1][4]))
        outfile.write(' W=%.3f P=%.3f \n' %(self.wilk[0],self.wilk[1]))
        # two-sided p-value for normality, low W indicates departure from normality thus high p-value

        outfile.write(" K2=%.3f P=%.3f, doesn't do a good job predicting normality for this case. \n" %(self.K2omnibus[0],self.K2omnibus[1]))
        #4.6 @10%, 6.0 <5%

##        outfile.write('Linear regression using probplot\n')
##        outfile.write('regression: a=%.2f b=%.2f, r = %.2f\n' % (self.m1,self.b1,self.r1))
        outfile.write(' Linear regression fit using probplot: r = %.2f\n' % (self.r1))
        
##        if run != 0 :
##            for i in range(4):
##                if wtype == 'create':
##                    outfile.writelines(str(self.soilDistributions[i].tolist()))
##                    outfile.write('\n')
##                elif wtype == 'read':
##                    outfile.writelines(str(self.soilDistributions[i]))
##    ##        else:
    ##            for i in range(len(self.X)):
    ##                outfile.writelines(str(self.X[i]))
    ##                outfile.write('\n')
        outfile.close()

    #the following critical values supplied in self.andy[1]
    ##Significance	Case 1	Case 2	Case 3	Case 4
    ##15%	1.610	 -	 -	0.576
    ##10%	1.933	0.908	1.760	0.656
    ##5%	2.492	1.105	2.323	0.787
    ##2.5%	3.070	1.304	2.904	0.918
    ##1%	3.857	1.573	3.690	1.092
    ##Case 1: The mean  and the variance  are both known.
    ##Case 2: The variance  is known, but the mean  is unknown.
    ##Case 3: The mean  is known, but the variance  is unknown.
    ##Case 4: Both the mean  and the variance  are unknown.
    ##for a normal distribution

    def updateStats(self):
               

        self.mean = sp.mean(self.X)
        self.sd = sp.std(self.X)

        #vals = sp.arange(1,len(X)+1)
        ranks = st.mstats.rankdata(self.X)
        ranks = sp.sort(ranks)

        # normalized ranks, using Bloms transformation/approximation
        self.Z = st.norm.ppf((ranks-0.375)/(len(ranks)+0.25))

        # linear regression, using mean and stddev.
        self.x = sp.array([-3,3])
        self.y = self.sd*self.x +  self.mean

        # ratio of IQR/stdev, calculations
        Q1 = st.scoreatpercentile(self.X,25)
        Q3 = st.scoreatpercentile(self.X,75)

        IQR = Q3 - Q1

        z1 = -0.67
        z3 =  0.67

        Q1z = (self.sd*z1) + self.mean
        Q3z = (self.sd*z3) + self.mean

        self.diff1 = abs(Q1 - Q1z)
        self.diff3 = abs(Q3 - Q3z)
        self.ratio = IQR/self.sd

        #Coefficient of Variation calculations, CV
        # 1.96 indicates 95% significance level
        Ek = self.sd/self.mean
        self.CV = Ek
        Ek2 = Ek*Ek
        
        temp = 1.96*(Ek2/(sqrt(len(self.X)-1)))*(0.5+Ek2)
        self.CI = [Ek-temp,Ek+temp]
        
        #shape tests
        (self.osm,self.osr),(self.m1,self.b1,self.r1) = st.probplot(self.X, fit=1, dist='norm')  
        self.osmf = self.osm.take([0, -1])  # endpoints 
        self.osrf = self.m1 * self.osmf + self.b1       # fit line
       
        self.k = st.kurtosis(self.X,fisher=False) #returns Pearson b2
        self.ktrue = st.kurtosistest(self.X) #returns Z-score, two-sided P-value
        self.s = st.skew(self.X)
        self.strue = st.skewtest(self.X) #returns two-sided P-value

        #goodness of fit tests
        self.andy = st.anderson(self.X, dist='norm')
        self.wilk = st.shapiro(self.X)
        self.K2omnibus = st.normaltest(self.X)
        samples = []
        for i in range(int(len(self.X)*0.10)):
            k = randrange(len(self.X))
            samples.append(self.X[k])
        if len(samples) > 10:
            self.sampleAndy = st.anderson(samples, dist='norm')
            self.sampleK2omnibus = st.normaltest(samples)
            self.sampleWilk = st.shapiro(samples)
        else:
            self.sampleAndy = [0.0000,[0.0000,0.0000,0.0000,0.0000,0.0000]]
            self.sampleK2omnibus = [0.0000,0.0000]

    def get_stats(self):
        return [self.ratio, self.k, self.s,self.andy,self.K2omnibus,self.sampleAndy,self.wilk]

    def get_data(self):
        return self.X

    def get_basicStats(self):
        return self.mean, self.sd

    def get_ratio(self):
        return self.ratio,self.diff1,self.diff3

    def get_kurtosis(self):
        return self.k,self.ktrue[1]/2
    
    def get_skewness(self):
        return self.s,self.strue[0]/2

    def show(self):
        plt.show()
    

