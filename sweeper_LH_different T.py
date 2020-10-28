import sys
sys.path.insert(0, 'C:\\Users\\vcostanz\\Desktop\\Linghui\\PYTHON\\MFIA_LH')
sys.path.append('C:\\Users\\vcostanz\\Desktop\\Linghui\\PYTHON\\TemperatureBoard_LH')
from MFIA_LH import MFIA
from TemperatureBoard import TemperatureBoard
from multicycles_LH import tempsweep
# import PyQt5
import datetime
import time
import pandas as pd
import numpy as np
deviceID = 'dev3275'
amplitude = 0.01
currentRange = 1e-6
demodRate = 100e3
samplingRate = 0.001
scan=0  # 0 sequential
accuracy=0  #0 is normal, 1 is high precision
path='C:\\Users\\vcostanz\\Desktop\\Linghui\\test_sweeper\\'
startFrequency = 1
endFrequency = 5e6
samples = 100  #number of sample points

##Temperature Settings##
frequency = '007-3'         ###Minimum Frequency 007-3
Tamplitude = '010'           ##percentage of the amplitude
temperature ='20.00'
charNumber = 5              ###DO NOT CHANGE
fileIDData =  'Tconstant_' + Tamplitude + ctime

temp = TemperatureBoard(port, baudRate)
temp.begin()



i=0
reI_now=[]
reI_pre=[]
port = 'COM5'
baudRate = 1000000

now = datetime.datetime.now()
ctime = now.strftime("%Y-%m-%d_%H%M")

#### TO DO: implement calibration reading ####
subDirectoryCalibration = 'C:\\Users\\vcostanz\\Desktop\\Vinnie\\'
fileIDCalibration = 'constant_c.txt'
#############################################
subDirectoryData =path  #KEVIN\\[0] Test starts here\\Polymer2_PET\\20191021\\' #Folder where the data are saved

Tdata = {'temperature': [], 'time': []}
Tdata["temperature"] = temp.pollData(charNumber)
file = temp.selectFile(subDirectoryData, fileIDData)
temp.writeDataToFile(file, Tdata, True)
### Path and name where data are saved ####
temp.setTemperature(temp.wave["pid"], temperature)
j=1
current_temp=temperature
while True:
    if i%2==0:
        scan=0 # sequential
    else:
        scan=3  # reverse

    lockIn = MFIA(deviceID)
    now = datetime.datetime.now()
    lockIn.set2TerminalMode(amplitude, startFrequency, currentRange, demodRate, samplingRate)
    lockIn.begin()
    time.sleep(2)
    ctime=now.strftime("%Y-%m-%d_%H%M")
    filename=str(amplitude)+'V_accuracy_'+str(accuracy)+'_scan_'+str(scan)+'_'+ctime+'_'+current_temp
    print(filename)
    lockIn.setAmplitude(0.01)
    lockIn.setFrequency(startFrequency)
    print('autorange')

    lockIn.sweeperSet(startFrequency, endFrequency, samples,scan,accuracy=accuracy)
    lockIn.sweeperStart()
    status = lockIn.sweeperStatus()
    lockIn.autoRange()

    print(status)
    while not status['done']:
        data = lockIn.pollData()
        data["temperature"] = temp.pollData(charNumber)
        time.sleep(1)
        data = lockIn.sweeperRead()
        end = time.time()
        Tdata["time"] = end
        temp.writeDataToFile(file, Tdata)
        # if not data['nan']: print(data)
        # if bool(data): print(data['nan'])
        status = lockIn.sweeperStatus()


    print(data.head(5))
    lockIn.sweeperClose()
    data.to_csv(path+filename+'.csv',sep='\t',index=False)
    reI_now=np.array(data['x'].values)


    if i!=0 and i%2==0 :
        diff = np.mean((reI_pre - reI_now) / reI_pre)
        print('difference is ',diff)
        reI_pre=reI_now

        if diff<0.050:
            if j<=3:
                temp.setTemperature(temp.wave["pid"], temperature)
                j += 1
                current_temp=temperature
                time.sleep(180)
            else:
                temp.closeFile(file)
                temp.disableOutput()
                print("Output Disabled")
                temp.end()

        # temp.setTemperature(temp.wave["pid"], Ttemperature)
        # time.sleep(60*30)
    else:
        reI_pre=np.array(data['x'].values)
    # lockIn.adjustRange(10e-9)

    instant = lockIn.pollData()
    i+=1