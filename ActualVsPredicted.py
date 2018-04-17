#Imports
import requests
from itertools import izip
from datetime import datetime
import csv
import xml.etree.ElementTree as ET
import collections
import glob

#Declarations
offSetList = []
time = []
myList = []
myList2 = []
myList3 = []
Ptime = []
Ptemp = []
Ptime = []
Ptemp = []
PredictedDate = []
PredictedTemperature = []
myActualDict = dict()
orignaltemp = []
ActualDate = []
ActualTemperature = []
Dict = dict()

"""This code extracts actual temperature observations from national weather service for comparison with predicted temperature observations"""
"""After Extraction forms a CSV file which contains columns for actual and predicted temperatures"""
"""Element Tree XML parser is used to get root and nodes inside the XML file in order to get the temperature values"""

csvNaming = 0
xml = requests.get("https://www.wrh.noaa.gov/mesowest/getobextXml.php?sid=LOAC1&num=360") #Actual Temperature values from the URL
xmlfiles = glob.glob(r'C:\Users\Aayush Goyal\IdeaProjects\Project2DS\project2files\*.xml') #Location of Predicted Temperature XML files collected from Schedule script
weatherXML = xml.text
root = ET.fromstring(weatherXML)
ActTime = []
object = root.findall("ob")
for i in range(len(object)):
    ut = object[i].attrib['utime']
    ts = str(datetime.utcfromtimestamp(float(ut)))   #Conversion of Unix Timestamp
    tm = ts + '-08:00'
    time.append(ts)
    ActTime.append(tm)
r = root.findall("ob/variable")
for y in range(len(r)):
    if r[y].attrib['description'] == 'Temp':
        t = r[y].attrib['value']
        orignaltemp.append(t)
for p in range(len(orignaltemp)):
    Dict[ActTime[p]] = orignaltemp[p]
Dict = collections.OrderedDict(sorted(Dict.items()))  # KeysSorted

for xml in xmlfiles:
    with open(xml) as file:
        csvNaming = csvNaming + 3
        tree = ET.parse(xml)
        timelayout = tree.findall("data/time-layout")
        temp_parameter = tree.findall("data/parameters/temperature")
        Dt = timelayout[2]
        for abc in range(1, 33):
            for i in range(abc, abc+1):
                for j in range(i, i+1):
                    mp = Dt[i].text.split('T')
                    z = mp[0] + ' ' + mp[1]
                    Ptime.append(z)
                TempData = temp_parameter[2]
                for z in range(i, i+1):
                    mp = TempData[z].text
                    Ptemp.append(mp)
            #DataCollection

            Predict = dict(zip(Ptime, Ptemp))
            Predict = collections.OrderedDict(sorted(Predict.items()))
            print "myActualDict", myActualDict
            print "Predict", Predict
            for wp in myActualDict:
                if wp in Predict:
                    ActualDate.append(wp)
                    ActualTemperature.append(Predict[wp])

            for qp in Predict:
                if qp in myActualDict:
                    PredictedDate.append(qp)
                    PredictedTemperature.append(myActualDict[qp])
            N = str(csvNaming) + "HrsFromNow.csv"       #Automatic_Naming
            print N
            with open(N, 'wb') as f:
                writer = csv.writer(f)
                writer.writerows(izip(ActualDate, ActualTemperature, PredictedDate, PredictedTemperature)) # Columns of Actual and Predicted temperature values
