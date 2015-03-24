## clustering.py
## Derek Groenendyk
## 9/11/2014
##

import numpy as np

class USDAClustering(object):
    def __init__(self):
        self.srcDrive = 'C:\\Derek\\'
        self.importSSCData()
        self.setClasses()
        self.USDATriangleDict()
 
    @property
    def SSC_Data(self):
        return self._SSC_Data
    @SSC_Data.setter
    def SSC_Data(self, value):
        self._SSC_Data = value

    @property
    def srcDrive(self):
        return self._srcDrive
    @srcDrive.setter
    def srcDrive(self, value):
        self._srcDrive = value

    @property
    def classes(self):
        return self._classes
    @classes.setter
    def classes(self, value):
        self._classes = value
 
    @property
    def classDict(self):
        return self._classDict
    @classDict.setter
    def classDict(self, value):
        self._classDict = value

    @property
    def classification(self):
        return self._classification
    @classification.setter
    def classification(self, value):
        self._classification = value

    @property
    def classVariable(self):
        return self._classVariable
    @classVariable.setter
    def classVariable(self, value):
        self._classVariable = value

    def importSSCData(self):       
        infile = open(self.srcDrive+'ProgrammingFolder\\Projects\\SSC.txt','r')
        lines = infile.readlines()
        infile.close()
        mdata = [[float(s.split()[i+1]) for i in range(3)] for s in lines[1:len(lines)]]
        self.SSC_Data = np.array(mdata)
        # table = mdata
        # sorts the the columns of sand, silt and clay in this order and descending in value
        # cols = [0,1,2]
        # for col in reversed(cols):
        #     table = sorted(table, key=operator.itemgetter(col))[::-1]
        # table = np.array(table)
        # table[:,[2,1]] = table[:,[1, 2]]        
        # inc = max(table[1,0:3]-table[2,0:3])

    def defineClass(self,ssc):

        sand = ssc[0]
        silt = ssc[1]
        clay = ssc[2]

        # if silt+1.5*clay < 15:
        if silt+1.5*clay < 12:
            classification = 'sand'
        # elif silt+1.5*clay >= 15 and silt+2.0*clay < 30:
        elif silt+1.5*clay >= 12 and silt+2.0*clay < 30:
            classification = 'loamy sand'
        # elif (silt+2.0*clay >= 30 and sand > 52 and clay < 20 and clay >= 7) or (clay < 7 and silt < 50 and silt+2.0*clay >= 30):
        elif (silt+2.0*clay >= 30 and sand > 52 and clay < 20 and clay >= 7) or (clay < 7 and silt < 52 and silt+2.0*clay >= 30):
            classification = 'sandy loam'
        # elif sand <= 52 and silt < 50 and silt >= 28 and clay < 27 and clay >= 7:
        elif sand <= 52 and silt < 52 and silt >= 28 and clay < 27 and clay >= 7:
            classification = 'loam'
        # elif (silt >= 50 and clay >= 12 and clay < 27) or (silt >= 50 and silt < 80 and clay < 12):
        elif (silt >= 52 and clay >= 14 and clay < 27) or (silt >= 52 and silt < 82 and clay < 14):
            classification = 'silt loam'
        # elif silt >= 80 and clay < 12:
        elif silt >= 82 and clay < 14:
            classification = 'silt'
        elif sand > 45 and silt < 28 and clay >= 20 and clay < 35:
            classification = 'sandy clay loam'
        elif sand > 20 and sand <= 45 and clay >= 27 and clay < 40:
            classification = 'clay loam'
        elif sand <= 20 and clay >= 27 and clay < 40:
            classification = 'silty clay loam'
        # elif sand > 45 and clay >= 35:
        elif sand > 45 and clay >= 35:
            classification = 'sandy clay'
        # elif silt >= 40 and clay >= 40:
        elif silt >= 42 and clay >= 40:
            classification = 'silty clay'
        # elif sand <= 45 and silt < 40 and clay >= 40:
        elif sand <= 45 and silt < 42 and clay >= 40:
            classification = 'clay'

        try:
            return classification
        except UnboundLocalError:
            print(ssc)

        
    def USDATriangleDict(self):
        self.classification = []

        for soil in self.SSC_Data:
            texClass = self.defineClass(soil)
            self.classification.append(texClass)

        # self.classDict = dict(zip(range(1326),classification))

        self.classVariable = np.array([self.classes.index(item) for item in [self.classification[i] for i in range(1326)]])

        # print([classDict[i+1300] for i in range(20)])

    def setClasses(self):
        classes = [ 'Sand',
                    'Loamy Sand',
                    'Sandy Loam',
                    'Loam',
                    'Silt Loam',
                    'Silt',                
                    'Sandy Clay Loam',
                    'Clay Loam',
                    'Silty Clay Loam',
                    'Sandy Clay',
                    'Silty Clay',
                    'Clay']
        self.classes = [item.lower() for item in classes]
