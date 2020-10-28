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
import os



deviceID = 'dev3275'
amplitude = 0.01
currentRange = 1e-6
demodRate = 100e3
samplingRate = 0.001
scan=0  # 0 sequential
accuracy=0  #0 is normal, 1 is high precision
path='C:\\Users\\vcostanz\\Desktop\\Linghui\\test_sweeper\\'
startFrequency = 1000
endFrequency = 5e4
IS_temperature = '20.00'

samples = 100  # number of sampling points in each sweep
wait_time=0.1   # time to wait for temperature equilibrium (min)


##Temperature Sweeping Settings##
frequency = '007-3'         ###Minimum Frequency 007-3
Tamplitude = '010'           ##percentage of the amplitude
charNumber = 5              ###DO NOT CHANGE
temperature_sweep_time=20    ### Time for temperature sweeping between impedance spect (min)
offset = '+00'              ##offset with respect to room temperature
tempdir = os.path.join(path, "tsweep\\")   ## the dir for temp sweep data
if not os.path.exists(tempdir):
    os.mkdir(tempdir)

##Electrical Settings##
voltage=0.01


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
subDirectoryData =path+'tsweep\\'  #KEVIN\\[0] Test starts here\\Polymer2_PET\\20191021\\' #Folder where the data are saved

fileIDData =  'Tconstant_' + Tamplitude + ctime

temp = TemperatureBoard(port, baudRate)
temp.begin()
temp.setTemperature(temp.wave["pid"], IS_temperature)
Tdata = {'temperature': [], 'time': []}
Tdata["temperature"] = temp.pollData(charNumber)
file = temp.selectFile(subDirectoryData, fileIDData)
temp.writeDataToFile(file, Tdata, True)
### Path and name where data are saved ####

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
    filename=str(amplitude)+'V_accuracy_'+str(accuracy)+'_scan_'+str(scan)+'_'+ctime
    print(filename)
    lockIn.setAmplitude(voltage)
    lockIn.setFrequency(startFrequency)
    lockIn.autoRange()
    print('autorange')

    lockIn.sweeperSet(startFrequency, endFrequency, samples,scan,accuracy=accuracy)
    lockIn.sweeperStart()
    status = lockIn.sweeperStatus()

    print(status)
    # while not status['done']:
    #     time.sleep(1)
    #     data = lockIn.pollData()
    #     tempdata= temp.pollData(charNumber)
    #     time.sleep(1)
    #     data = lockIn.sweeperRead()
    #     # end = time.time()
    #     if not data['nan']:
    #        print(data['nan'])
    #     # # Tdata["time"] = end
    #     #      temp.writeDataToFile(file, data)
    #     # if not data['nan']: print(data)
    #     # if bool(data): print(data['nan'])
    #     status = lockIn.sweeperStatus()
    while not status['done']:
        time.sleep(1)
        data = lockIn.sweeperRead()
        # if not data['nan']: print(data)
        if len(data)==0:
            print('no data')
        status = lockIn.sweeperStatus()

    print(data.head(5))
    lockIn.sweeperClose()
    data.to_csv(path+filename+'.csv',sep='\t',index=False)
    reI_now=np.array(data['x'].values)


    if i!=0 and i%2==0 :
        diff = np.abs(np.mean((reI_pre - reI_now) / reI_pre))
        print('difference is ',diff)
        reI_pre=reI_now
        #
        # if diff<0.10:
        tempsweep(temperature_sweep_time,tempdir)

        temp.setTemperature(temp.wave["pid"], IS_temperature)
        time.sleep(60*wait_time)
    else:
        reI_pre=np.array(data['x'].values)
    # lockIn.adjustRange(10e-9)

    instant = lockIn.pollData()
    i+=1