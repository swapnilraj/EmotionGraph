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
    csv = pandas.read_csv(name, sep="\",\"") 
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
        maxval = 0
        emotion = ""
        for col in criteria:
            try:
                val = float(csv.lookup([row], [col])[0])
            except ValueError:
                val = float(csv.lookup([row], [col])[0][0:-1])
            except TypeError:
                pass
            print col, val
            if val > maxval:
                print "bigger"
                emotion = col
                maxval = val
        print "Chose " + emotion, maxval
        timeEmotionTuples.append((csv.lookup([row], ["time"])[0], emotion))
    return timeEmotionTuples

elist = getEmotionList(readfile(selectCSV(listCSVs())), ["joy","disgust","sadness","fear","anger"])

data = ""
for time, emotion in elist:
    data += "%s,%s\n" % (time, emotion)

f = open("test.csv", "w")
f.write(data)
f.close()
print data
