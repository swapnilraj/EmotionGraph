import pandas
import os
import fnmatch

def listCSVs():
    csvList = []
    for filename in os.listdir('.'):
        if fnmatch.fnmatch(filename, '*.csv'):
            csvList.append(filename)
    return csvList

def readfile(name):
    csv = pandas.read_csv(name) 
    return csv

def getArray(csv, title):
    pass

def selectCSV(csvList):
    while True:
        for index, filename in enumerate(csvList):
            print("%d, %s" % (index, filename))
        selectIndex = input()
        if selectIndex < len(csvList):
            return csvList[selectIndex]
        else:
            print("Invlaid selection.")

print(readfile(selectCSV(listCSVs())).time)