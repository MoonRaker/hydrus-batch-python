## FTH_Data_Class.py
## Derek Groenendyk
## 5/23/2012
## gets the ET, BM, SM, and yield data for the FTH treatment

from win32com.client import *
from hydrus import excel
import os
import numpy as np

class FTHData:

    def __init__(self,filename):
        # Excel object
        self.excel = excel.Excel()
        self.excel.openExcel()
        
        # workbook used to work with the data
        self.filename = filename

    def openWorkBook(self):
        self.workbook = self.excel.openWorkBook(self.filename)

    def closeWorkBook(self):
        self.workbook.Close(True)
        # if no more books are open close excel?
        self.excel.closeExcel()

    def showWorkBook(self):
        self.excel.setVis(True)
        
    def hideWorkBook(self):
        self.excel.setVis(False)

    def readET(self,year,param):
        name = 'ET'

        sheet = self.workbook.Sheets(name)
        offset = 0
        if 'seepage' in param.lower():
            offset += 2
        if 'cumulative' in param.lower():
            offset += 1

        if year == '04':
            numDays = 22
            startRow = 25
            data = np.zeros((numDays+1,5))
            DOYOffset = 21  # 28 days between DOY 8 and planting DOY 344, minus the 7 warm-ups days
        else:
            numDays = 23
            startRow = 55
            data = np.zeros((numDays+1,5))
            print '\n Double check DOY offset!!\n'
            DOYOffset = 18

        for day in range(numDays):
            row = day + startRow

            data[day+1,:] = [sheet.Cells(row,3).Value+DOYOffset,sheet.Cells(row,5+offset).Value,sheet.Cells(row,9+offset).Value,
                           sheet.Cells(row,13+offset).Value,sheet.Cells(row,17+offset).Value]

        return data

    def readBiomass(self,year,param='bio'):
        if year == '04':
            sheet = '03-04 Biomass'
        else:
            sheet = '04-05 Biomass'

        sheet = self.workbook.Sheets(sheet)
        numDays = sheet.UsedRange.Rows.Count+1-4

        data = None
        dates = np.zeros((1,2))
##        print dates
        offset = 0
        if param.lower() == 'glai':
            offset = 4

        for day in range(numDays):
            row = day + 5
            if sheet.Cells(row,5+offset).Value != None:
                temp = np.array(sheet.Cells(row,4).Value)
                temp = np.append(temp,np.array(sheet.Range(sheet.Cells(row, 5+offset),sheet.Cells(row, 8+offset)).Value)[0])
                tempDates = [[sheet.Cells(row, 2).Value],[sheet.Cells(row, 4).Value]]
                if data == None:
                    data = np.array([temp])
                    dates = tempDates
                else:
                    data = np.concatenate((data,np.array([temp])))
                    dates = [np.append(dates[i],tempDates[i]) for i in range(2)]
                    

        return data,dates

    def readWater(self,year,layer,depth=30):
        if year == '04':
            sheet = '03-04 Soil Moisture'
        else:
            sheet = '04-05 Soil Moisture'

        sheet = self.workbook.Sheets(sheet)
        numDays = sheet.UsedRange.Rows.Count+1-4

        data = None
        if depth == 30:
            offset = 0
        else:
            offset = round(depth/30)*4

        offset = (layer-2)*4
        if layer - 2 < 0:
            offset = 0

##        print 'offset',offset
        for day in range(numDays):
            row = day + 5
            if sheet.Cells(row,5+offset).Value != None:
                temp = np.array(sheet.Cells(row,3).Value)
                temp = np.append(temp,np.array(sheet.Range(sheet.Cells(row, 5+offset),sheet.Cells(row, 8+offset)).Value)[0])
                if data == None:
                    data = np.array([temp])
                else:
                    data = np.concatenate((data,np.array([temp])))
                    
        return data

    def readYield(self,year):
        name = 'Yield'

        sheet = self.workbook.Sheets(name)

        if year == '04':
            data = np.array(sheet.Range(sheet.Cells(5,2),sheet.Cells(8,2)).Value).flatten()
        else:
            data = np.array(sheet.Range(sheet.Cells(5,5),sheet.Cells(8,5)).Value).flatten()

        return data
