## Excel_Class.py
## Derek Groenendyk
## 5/23/2012
## creates an excel object for working with excel workbooks

from win32com.client import *
import os
import numpy as np

class Excel:

    def __init__(self):
        pass

    def openExcel(self):
        self.excel = Dispatch('Excel.Application')

    def closeExcel(self):
        self.excel.Visible = True
        self.excel.Quit()
        del self.excel
        
    def setVis(self,boolean):
        self.excel.Visible = boolean

    def openWorkBook(self,filename):
        #opens the workbook    
        self.workbook = self.excel.Workbooks.Open(filename)
        return self.workbook  

    def createSheet(self,workbook,name):
        #creates a new worksheet if it doesn't already exist
        for sheet in workbook.Sheets:
            if sheet.name == name:
                flag = True
                break
            else:
                flag = False
        if not flag:
            workbook.Worksheets.Add().Name = name

    def createBook():
        # creates the workbook if it doesn't already exist
        if not os.path.exists(filename):
            NewBook = workbooks.Add()
            NewBook.SaveAs(filename)
