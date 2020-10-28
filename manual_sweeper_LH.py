import sys
sys.path.insert(0, 'C:\\Users\\vcostanz\\Desktop\\Linghui\\PYTHON\\MFIA_LH')
# sys.path.append('C:\\Users\\vcostanz\\Desktop\\Linghui\\PYTHON\\TemperatureBoard_LH')

sys.path.append('C:\\Users\\vcostanz\\Desktop\\Pyhton Projects\\TemperatureBoard')
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

amplitude = 0.01   # voltage IS
currentRange = 1e-6  # autorange suggested

demodRate = 100e3
samplingRate = 0.001
scan=0  # 0 sequential
accuracy=0  #0 is normal, 1 is high precision

path='C:\\Users\\vcostanz\\Desktop\\Linghui\\test_sweeper\\'
startFrequency = 1000
endFrequency = 5e6
IS_temperature = '25.00'
samples = 50  # number of sampling points in each sweep
wait_time=0.5   # time to wait for temperature equilibrium (min)
frequencies=np.logspace(np.log10(startFrequency), np.log10(endFrequency), num=samples)
print(frequencies)
##Temperature Sweeping Settings##
frequency = '007-3'         ###Minimum Frequency 007-3
Tamplitude = '010'           ##percentage of the amplitude
charNumber = 5              ###DO NOT CHANGE

temperature_sweep_time=12   ### Time for temperature sweeping between impedance spect (min)
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


# Tdata = {'temperature': [], 'time': []}
# Tdata["temperature"] = temp.pollData(charNumber)
# file = temp.selectFile(subDirectoryData, fileIDData)
# temp.writeDataToFile(file, Tdata, True)
### Path and name where data are saved ####

while True:
    if i%2==0:
        scan=0 # sequential
    else:
        scan=3  # reverse
    temp = TemperatureBoard(port, baudRate)
    temp.begin()
    temp.setTemperature(temp.wave["pid"], IS_temperature)

    lockIn = MFIA(deviceID)
    now = datetime.datetime.now()
    lockIn.set2TerminalMode(amplitude, startFrequency, currentRange, demodRate, samplingRate)
    #  For temperatire to adjust time.sleep(20)
    print('Temperature:',temp.pollData(charNumber))
    ctime=now.strftime("%Y-%m-%d_%H%M")
    filename=str(amplitude)+'V_accuracy_'+str(accuracy)+'_scan_'+str(scan)+'_'+ctime
    print(filename)
    file = temp.selectFile(path, filename)

    lockIn.setAmplitude(voltage)
    lockIn.setFrequency(startFrequency)
    lockIn.begin()

    # lockIn.autoRange()
    print('autorange')
    reI_now=[]
    #     status = lockIn.sweeperStatus()
    ss=time.time()
    for f in frequencies:
        lockIn.setFrequency(f)   ###  Why time constant is 10/f in MFIA??
        time.sleep(5/f)
        print(f)
        while True:
            time.sleep(1)
            oridata = lockIn.pollData()
            print(oridata)
            range_exp = np.round(np.log10(oridata['abs'])) + 2
            if len(oridata)==0:
                print('no data')
            elif currentRange!=range_exp:
                ### check the range

                ###Could have infinite loop!!!!!!!!!!!!!!!!
                while True:
                    lockIn.adjustRange(10**(range_exp))
                    time.sleep(1)
                    data = lockIn.pollData()
                    print('range adjustment:',10**(range_exp))
                    newrange_exp=np.round(np.log10(data['abs']))+2
                    if newrange_exp == range_exp:
                        currentRange = range_exp
                        break
                    range_exp =newrange_exp
                data["temperature"] = temp.pollData(charNumber)
                data['frequency'] = f
                reI_now.append(data['abs'])
                temp.writeDataToFile(file, data)
            else:
                # print('data finish')
                data=oridata
                data["temperature"] = temp.pollData(charNumber)
                data['frequency'] = f
                reI_now.append(data['abs'])
                temp.writeDataToFile(file, data)
                break
        print('data',data)
    print('Finished one sweep,time ',time.time()-ss)
    print(data)
    reI_now=np.array(reI_now)
    # data.to_csv(path+filename+'.csv',sep='\t',index=False)



    if i!=0: #and i%2==0 :
        diff = np.abs(np.mean((reI_pre - reI_now) / reI_pre))
        reI_pre = reI_now
        print('difference is ',diff)        #
        if diff<0.10:
            temp.disableOutput()
            print("Output Disabled")
            temp.end()
            tempsweep(temperature_sweep_time,subDirectoryData)
            time.sleep(60*wait_time)

    else:
        reI_pre = reI_now

    # lockIn.adjustRange(10e-9)

    instant = lockIn.pollData()
    i+=1