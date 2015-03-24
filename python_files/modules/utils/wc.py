#SC_Class.py
#Created by Derek Groenendyk
#11/13/2011

import numpy as np
import scipy as sp
import matplotlib as mp
import matplotlib.pyplot as plt


class WC:

    def __init__(self):
        self.name = 'WC'
        self.srcDrive = "C:\\Derek\\"
       

    ## Calculate water content for a range of pressure heads
    def averageWC(self,heads,params):

        wc = []
        for head in heads:
            wc.append(self.calcWC(params,head))

        return wc

    ## Calculate Van Genuchten water content based on pressure heads
    def calcWC(self,params,head):
        
        theta_r = params[0]
        theta_s = params[1]
        alpha = params[2]
        n = params[3]
        K_s = params[4]

        m = 1.0-1.0/n

        vGWC = theta_r + (theta_s - theta_r)/((1.0+(alpha*abs(head))**n)**m)

        return vGWC


    ## Read in soil parameters
    def getParams(self):
        
        infile = open(self.srcDrive+'\\ProgrammingFolder\\Projects\\newSoilProps.txt','r')
        lines = infile.readlines()
        infile.close()

        paramValues = np.zeros((1326,5))

        i = -1
        for line in lines:
            i += 1
            data = line.split()
            for j in range(5):
                if j == 2:
                    # round and convert Alpha, to cm/day
                    temp = round(float(data[j+1])/100.0,4)
                elif j == 4:
                    # round and convert Ks, to cm/day
                    temp = round((float(data[j+1])*100.0)*(60*60*24),2)
                else:
                    temp = round(float(data[j+1]),4)
                                 
                paramValues[i,j] = temp

        return paramValues

    def getSSC(self):
        
        infile = open(self.srcDrive+'\\ProgrammingFolder\\Clustering Project\\newSoilTex.txt','r')
        lines = infile.readlines()
        infile.close()

        paramValues = np.zeros((1326,3))

        i = -1
        for line in lines:
            i += 1
            data = line.split()
            for j in range(3):
                temp = data[j+1]
                                 
                paramValues[i,j] = temp

        return paramValues


    def plotWC(self,wc):

        fig=plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(wc)
        ax.set_xlabel('Days')
        ax.set_ylabel('$\\theta$, cm$^3$/cm$^3$')

        ax.set_xticklabels(['1','2','3','4','5'])
       
    ##    ax.set_ylim((0,0.025))
    ##    ax.set_xlim((0,0.2))
        plt.show()

    def vanGsm(self,params,psi):

        # paramList = ['thr','ths','Alfa','n','Ks']
       
        m = 1.0-(1.0/params[3])

        theta = lambda h:  params[0] +(params[1]-params[0])*(1.0/(1.0+((params[2]*np.abs(h))**params[3])))**m

        wc = theta(psi)

        return wc


    def vGMKs(self,params,psi):

        m = 1.0-(1.0/params[3])

        a = 1.0+(params[2]*psi)**params[3]
        b = 1.0-(params[2]*psi)**(params[3]-1)

        Ks = params[4]*((b*(a)**-m)**2.0)/(a**(m/2.0))

        return Ks
   

    def vGKs(self,params,theta):

        m = 1.0-(1.0/params[3])

        a = (theta-params[0])/(params[1]-params[0]) # theta must be larger than theta_residual (thr)

        Ks = params[4]*(a**0.5)*((1.0-(1.0-a**(1.0/m))**m)**2.0)

        return Ks

    def vGKsSat(self,params,S):

        m = 1.0-(1.0/params[3])

        a = S

        Ks = params[4]*(a**0.5)*((1.0-(1.0-a**(1.0/m))**m)**2.0)

        return Ks
        

##def main():
##
##    srcDrive = "E:\\"
##    
##    exp = "SW605"
##    
##    ExpFileLocation = srcDrive+"ProgrammingFolder\\HYDRUS_Data\\Projects\\"+exp
##
##    NodInfOUT = NODINF(ExpFileLocation)
##    selectorIN = SELECTORIN(ExpFileLocation)
##
##    paramList = ['thr','ths','Alfa','n','Ks']
##    paramData = []
##    
##    for param in paramList:
##        paramData.append(float(selectorIN.getData(param)))
##
##    headData = NodInfOUT.getAvgHeadData(50)
##    print np.shape(headData)
##
##    wc = averageWC(headData,paramData)
##
##    plotWC(wc)
##
##
##if __name__=='__main__':
##    main()






























    

        
