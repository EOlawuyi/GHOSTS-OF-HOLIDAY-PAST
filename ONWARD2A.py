from PIL import Image as im
import sys
import numpy as np
import imageio.v3 as iio
import ipympl
import matplotlib.pyplot as plt
import skimage as ski
import skimage.feature
import pandas as pd
from skimage import feature, measure
from skimage.measure import label, regionprops, regionprops_table
import pyarrow.parquet as pa
import string
from openpyxl import load_workbook
from openpyxl import Workbook
import openpyxl
import csv

#This is the code that belongs to Olorogun Engineer Enoch O. Ejofodomi in his Collaboration with Shell Onward.
#This code also belongs to Engineer Francis Olawuyi in his collaboration with Shell Onward.
#The code also belongs to the following people
#1. Esther Olawuyi
#2. Michael Olawuyi.
#3. Joshua Olawuyi
#4. Joseph Olawuyi
#5. Onome Ejofodomi
#6. Efejera Ejofodomi
#7. Deborah Olawuyi
#8. Isi Omiyi
#9. Kome Odu
#10. Sunday Damilola Olawuyi
#11. Godswill Ofualagba
#12. Matthew Olawuyi
#13. Jason Zara
#14. Vesna Zderic
#15. Ahmed Jendoubi
#16. Mohammed Chouikha
#17. Shani Ross
#18. Nicholas Monyenye
#19. Ochamuke Ejofodomi
#20. 
# FEBRUARY 20, 2024.



#Read in Data for Scrooge in Table Format
table = pa.read_table('scrooge_bldg.parquet') 
table
table.shape
df = table.to_pandas() 
# Taking tanspose so the printing dataset will easy. 
df.head().T
data2 = df.head().T
print(data2)
data = df.head()
tcolumns = table.num_columns
trows = table.num_rows
column1 = table.columns[0]
data.size
data.shape
print(data)
data1 = np.array(data)
imageppp = np.asanyarray(data)
print(imageppp)
np.save('scrooge.txt',data)
#print(df.head().T[1])
#December Electricity Data is 2019 rows

#Official Code Starts Here

#Read in Scrooge Data for 2018
df = pd.read_parquet('scrooge_bldg.parquet')

#Convert file from parquet to csv in excel
df.to_csv('scrooge1.csv')

#Read CSV file
datacsv = pd.read_csv("scrooge1.csv")

#Geg Shape of Data in File
datacsv.shape

#Print Data
print(datacsv)

#Get Shape of CSV Data
[a,b] =  datacsv.shape
datacsv.values[0,1]

#datacsv.values[32062,:]
#data5= np.zeros((2019,b))

#Get Scrooge Data as from December 1, 2018 until the last available date of December 21, 2018
december = datacsv.values[32064:34080,:]

#Get shape of December Data
[a1,b1] =  december.shape

#forecast1= np.zeros((2977,b1))

#Variable to sum December Data for Scrooge per column
forecast2= np.zeros((1,b1))
#Variable to forecast the Load for Scrooge from December 22, 2018 to December 31, 2018 per column
forecastdata= np.zeros((960,b1))

#forecast1[0:2017,3:b1] = december[:,3:b1]
#forecastdata[0:2017,3:b1] = december[:,3:b1]

#Get shape of sum December Data for Scrooge
[a2,b2] =  forecast2.shape


#Test Code
#starta = [1,2,3,4,5]
#y = sum(starta[0:4])

#start= np.zeros((3,2))
#start[0,0] = 1
#start[0,1] = 2
#start[1,0] = 3
#start[1,1] = 4
#start[2,0] = 5
#start[2,1] = 6

#z = sum(start[0:2,1])


#Loop to sum all the load in Scrooge's house for the provided selected period of December 1 - December 21, 2018.
for j in range(2,b1):
    forecast2[0, j] = sum(december[:,j])

#Variable to hold consecutive Summation of Electricity Forecasted Data
sumvalue= forecast2
count = 0
#Nested Loop to forecast Scrooge's Electricity Load from December 22, 2018 till December 31, 2018
for i in range(0,960):
    for j in range(2,b1):
        if(i ==0):
            #if this is the first forecasted load, forecast based on
            #taking the average of Scrooge's Electricity Load from
            #December 1, 2018 till December 21, 2018
            forecastdata[i,j] = (forecast2[0, j])/120
            #Add Time Stamp Index to ForeCasted Data
            forecastdata[i,1] = count
        #if this is not the first foecasted load,
        #Summation the Electricity Data available to include already
        #forecasted Data after December 21, 2022
        sumvalue[0, j] = sumvalue[0, j] + forecastdata[i, j]
        #Forecast the present Electricity Load for the current time stamp
        #Between December 22, 2018, and December 31, 2018/ 
        forecastdata[i,j] = (sumvalue[0, j]/(b1+1+i) )
        #Add Time Stamp Index to ForeCasted Data
        forecastdata[i,1] = count
    count = count+1

#Get Electrcity load from December 22, 2018 till December 31, 2018
#betweem the time frame 8 p.m. - 12 a.m. (4 hrs)
#as this is the cheapest time each day to hold Scrooge's Party.

#variable to hold the cheapest 4 hour time between
#December 22 and December 31, 2018
cheapesttime= np.zeros((160,b1))

cheapesttime[0:15,:] = forecastdata[80:95,:]
cheapesttime[16:31,:] = forecastdata[176:191,:]
cheapesttime[32:47,:] = forecastdata[272:287,:]
cheapesttime[48:63,:] = forecastdata[368:383,:]
cheapesttime[64:79,:] = forecastdata[464:479,:]
cheapesttime[80:95,:] = forecastdata[560:575,:]
cheapesttime[96:111,:] = forecastdata[656:671,:]
cheapesttime[112:127,:] = forecastdata[756:757,:]
cheapesttime[128:143,:] = forecastdata[848:863,:]
cheapesttime[144:159,:] = forecastdata[944:959,:]

print(cheapesttime)


#Select the Three Appliances Selected for Scrooge's Party Cost
#variable to hold the 3 Appliances between December 22 and December 31, 2018
appliancerow= np.zeros((160,3))

#Select the columns in Cheapesttime that hold the 3 Requested Appliances for
#Scrooge's Party
#out.electricity.heating_hp_bkup.energy_consumption is column 17 in
#cheapesttime variable
#out.electricity.heating.energy_consumption is column 19 in
#cheapesttime variable
#out.electricity.plug_loads.energy_consumption is column 35 in
#cheapesttime variable
appliancerow[0:15,0] = cheapesttime[0:15,17]
appliancerow[0:15,1] = cheapesttime[0:15,19]
appliancerow[0:15,2] = cheapesttime[0:15,35]
appliancerow[16:31,0] = cheapesttime[16:31,17]
appliancerow[16:31,1] = cheapesttime[16:31,19]
appliancerow[16:31,2] = cheapesttime[16:31,35]
appliancerow[32:47,0] = cheapesttime[32:47,17]
appliancerow[32:47,1] = cheapesttime[32:47,19]
appliancerow[32:47,2] = cheapesttime[32:47,35]
appliancerow[48:63,0] = cheapesttime[48:63,17]
appliancerow[48:63,1] = cheapesttime[48:63,19]
appliancerow[48:63,2] = cheapesttime[48:63,35]
appliancerow[64:79,0] = cheapesttime[64:79,17]
appliancerow[64:79,1] = cheapesttime[64:79,19]
appliancerow[64:79,2] = cheapesttime[64:79,35]
appliancerow[80:95,0] = cheapesttime[80:95,17]
appliancerow[80:95,1] = cheapesttime[80:95,19]
appliancerow[80:95,2] = cheapesttime[80:95,35]
appliancerow[96:111,0] = cheapesttime[96:111,17]
appliancerow[96:111,1] = cheapesttime[96:111,19]
appliancerow[96:111,2] = cheapesttime[96:111,35]
appliancerow[112:127,0] = cheapesttime[112:127,17]
appliancerow[112:127,1] = cheapesttime[112:127,19]
appliancerow[112:127,2] = cheapesttime[112:127,35]
appliancerow[128:143,0] = cheapesttime[128:143,17]
appliancerow[128:143,1] = cheapesttime[128:143,19]
appliancerow[128:143,2] = cheapesttime[128:143,35]
appliancerow[144:159,0] = cheapesttime[144:159,17]
appliancerow[144:159,1] = cheapesttime[144:159,19]
appliancerow[144:159,2] = cheapesttime[144:159,35]


#0 = December 22
#16 = December 23
#32 = December 24
#48 = December 25
#64 = December 26
#80 = December 27
#96 = December 28
#112 = December 29
#128 = December 30
#144 = December 31

print(appliancerow)

#calculate the total party cost for the ten days selected
partycostsum = np.zeros((10,1))

#calculate the total party cost for each day between December 22 and
#December 31, 2018.
partycostsum[0] = sum(appliancerow[0:15,0]) + sum(appliancerow[0:15,1]) + sum(appliancerow[0:15,2]) 
partycostsum[1] = sum(appliancerow[16:31,0]) + sum(appliancerow[16:31,1]) + sum(appliancerow[16:31,2]) 
partycostsum[2] = sum(appliancerow[32:47,0]) + sum(appliancerow[32:47,1]) + sum(appliancerow[32:47,2]) 
partycostsum[3] = sum(appliancerow[48:63,0]) + sum(appliancerow[48:63,1]) + sum(appliancerow[48:63,2]) 
partycostsum[4] = sum(appliancerow[64:79,0]) + sum(appliancerow[64:79,1]) + sum(appliancerow[64:79,2]) 
partycostsum[5] = sum(appliancerow[80:95,0]) + sum(appliancerow[80:95,1]) + sum(appliancerow[80:95,2]) 
partycostsum[6] = sum(appliancerow[96:111,0]) + sum(appliancerow[96:111,1]) + sum(appliancerow[96:111,2]) 
partycostsum[7] = sum(appliancerow[112:127,0]) + sum(appliancerow[112:127,1]) + sum(appliancerow[112:127,2]) 
partycostsum[8] = sum(appliancerow[128:143,0]) + sum(appliancerow[128:143,1]) + sum(appliancerow[128:143,2]) 
partycostsum[9] = sum(appliancerow[144:159,0]) + sum(appliancerow[144:159,1]) + sum(appliancerow[144:159,2]) 

print("PartyCost Sum")
print(partycostsum)

#Get the date that holds the cheapest cost for Scrooge's Party

CheapestDay = min(partycostsum)
print("Cheapest Day:")
print(CheapestDay)


#Get the index row number for the chosen Date in variables Cheapest Day
# and ApplianceStartRow
ChosenDay = 0
ApplianceStartRow = 0  #Date of Party
for j in range(0,10):
    if(partycostsum[j] == CheapestDay):
        ChosenDay = j
        ApplianceStartRow = j*16


print("ChosenDay:")
print(ChosenDay)
print("ApplianceStartRow:")
print(ApplianceStartRow)


#Calculate the Party Load for the Selected Date and save it to a csv file.

#variable to store final Party Load Cost and the sum of the Three Appliances
#Load Cost and the Fixed Devices Load Cost for the Party
PartyLoad = np.zeros((16,3))
PartyLoad2 = np.zeros((16,1))

#Extract the Party Load Cost from the Chosen Date
PartyLoad = appliancerow[ApplianceStartRow: ApplianceStartRow + 15,:]
print("Party Load")
print(PartyLoad)

#Sum the cost of the three appliances for the chosen date as well as the
#Fixed Cost and put in Variable PartyLoad2
for i in range(0,16):
    PartyLoad2[i] = (0.3 * (appliancerow[i,0] + appliancerow[i,1] + appliancerow[i,2]) + 0.021) 
print("PartyLoad2: ")
print(PartyLoad2)


#Prepare Chosen Date Time Stamps for CSV File
datestamp1 = ""
timestamp1 = " 20:15:00"
timestamp2 = " 20:30:00"
timestamp3 = " 20:45:00"
timestamp4 = " 21:00:00"
timestamp5 = " 21:15:00"
timestamp6 = " 21:30:00"
timestamp7 = " 21:45:00"
timestamp8 = " 22:00:00"
timestamp9 = " 22:15:00"
timestamp10 = " 22:30:00"
timestamp11 = " 22:45:00"
timestamp12 = " 23:00:00"
timestamp13 = " 23:15:00"
timestamp14 = " 23:30:00"
timestamp15 = " 23:45:00"
timestamp16 = " 00:00:00"

#datestamp2 = datestamp + "111";
print(datestamp1)


finalstring = ["", "", "", "", "no", "", "", "", "", "", "", "", "", "" ,"", ""]
           #    "" "" "" "" "" "yes" "" "" "" "" "" "" "" "" "" ""]
print("Final String:")
print(finalstring)
print(finalstring[1])


if(ApplianceStartRow ==0):
    datestamp1 = "2018-12-22"
if(ApplianceStartRow ==16):
    datestamp1 = "2018-12-23"
if(ApplianceStartRow ==32):
    datestamp1 = "2018-12-24"
if(ApplianceStartRow ==48):
    datestamp1 = "2018-12-25"
if(ApplianceStartRow ==64):
    datestamp1 = "2018-12-26"
if(ApplianceStartRow ==80):
    datestamp1 = "2018-12-27"
if(ApplianceStartRow ==96):
    datestamp1 = "2018-12-28"
if(ApplianceStartRow ==112):
    datestamp1 = "2018-12-29"
if(ApplianceStartRow ==128):
    datestamp1 = "2018-12-30"
if(ApplianceStartRow ==144):
    datestamp1 = "2018-12-31"
print("ApplianceStartRow: ")
print(datestamp1)


finalstring[0] = datestamp1 + timestamp1
finalstring[1] = datestamp1 + timestamp2
finalstring[2] = datestamp1 + timestamp3
finalstring[3] = datestamp1 + timestamp4
finalstring[4] = datestamp1 + timestamp5
finalstring[5] = datestamp1 + timestamp6
finalstring[6] = datestamp1 + timestamp7
finalstring[7] = datestamp1 + timestamp8
finalstring[8] = datestamp1 + timestamp9
finalstring[9] = datestamp1 + timestamp10
finalstring[10] = datestamp1 + timestamp11
finalstring[11] = datestamp1 + timestamp12
finalstring[12] = datestamp1 + timestamp13
finalstring[13] = datestamp1 + timestamp14
finalstring[14] = datestamp1 + timestamp15
finalstring[15] = datestamp1 + timestamp16

print(finalstring[15])


#TimeStampDate = datacsv.values[32064:34080,1]
#print(TimeStampDate)

#Code is finished for now 
print("done")
#df = pd.DataFrame([[1,2,3], [4,5,6]])#,  columns=['a', 'b','c'])
df = pd.DataFrame( [[finalstring[0], PartyLoad2[0]], [finalstring[1], PartyLoad2[1]], [finalstring[2], PartyLoad2[2]], [finalstring[3], PartyLoad2[3]], [finalstring[4], PartyLoad2[4]], [finalstring[5], PartyLoad2[5]], [finalstring[6], PartyLoad2[6]], [finalstring[7], PartyLoad2[7]], [finalstring[8], PartyLoad2[8]], [finalstring[9], PartyLoad2[9]], [finalstring[10], PartyLoad2[10]], [finalstring[11], PartyLoad2[11]], [finalstring[12], PartyLoad2[12]], [finalstring[13], PartyLoad2[13]], [finalstring[14], PartyLoad2[14]], [finalstring[15], PartyLoad2[15]]],  columns=['timestamp', 'party_cost'])
df.to_csv('sample_submission2.csv')


#Read CSV file
datafile = pd.read_csv("sample_submission2.csv")

#Geg Shape of Data in File
datafile.shape

#Print Data
print("Datafile")
print(datafile)

