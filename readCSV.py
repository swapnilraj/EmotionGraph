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
    csv = pandas.read_csv(name, sep=", ") 
    return csv

def getSequences(csv, title):
    sequence = csv.filter(items=title)
    if not sequence.empty:
        return sequence
    else:
        print("No such title '%s'." % title)

def selectCSV(csvList):
    while True:
        for index, filename in enumerate(csvList):
            print("%d, %s" % (index, filename))
        selectIndex = input()
        if selectIndex < len(csvList):
            return csvList[selectIndex]
        else:
            print("Invlaid selection.")

def getEmotionList(csv, criteria):
    timeEmotionTuples = []
    for row in range(len(csv.index)):
        max = 0
        emotion = ""
        for col in criteria:
            val = lookup([row], [col])[0]
            if val > max:
                emotion = col
                max = val
        timeEmotionTuples.append((csv.lookup([row], ["time"])[0], emotion))
    return timeEmotionTuples

print(getEmotionList(readfile(selectCSV(listCSVs())), ["sadness", "fear"]))
