import sys
sys.path.insert(0, 'C:\\Users\\vcostanz\\Desktop\\Linghui\\PYTHON\\MFIA_LH')
# sys.path.append('C:\\Users\\vcostanz\\Desktop\\Linghui\\PYTHON\\TemperatureBoard_LH')

sys.path.append('C:\\Users\\vcostanz\\Desktop\\Pyhton Projects\\TemperatureBoard')
from MFIA_LH import MFIA
from TemperatureBoard import TemperatureBoard
from multicycles_LH import tempsweep
from multicycles_LH import constant_temperature

# import PyQt5
import datetime
import time
import pandas as pd
import numpy as np
import os
from autorange_current import autorange_current
import signal


deviceID = 'dev3275'

amplitude = 0.01  # voltage IS
currentRange = 1e-6  # autorange suggested

demodRate = 100e3
samplingRate = 0.001
scan=0  # 0 sequential
accuracy=0  #0 is normal, 1 is high precision

path='C:\\Users\\vcostanz\\Desktop\\Linghui\\P6\\P6ABA,CoCl2,1v2\\Taped\\'

# middleFrequency=50
# endFrequency = 5.2e6
IS_temperature = '20.00'
samples = 100  # number of sampling points in each sweep
wait_time=0   # time to wait for temperature equilibrium (min)
Dehydrate_temperature='65.00'

## Frequency ranges
frequency_end=[10,100,1e4,1e5,1e6]
frequency_start=[1,10,100,1e4,1e5]
startFrequency=frequency_start[0]
npoint=[15,25,50,25,25]

##Temperature Sweeping Settings##
temperature_sweep_time=3 ### Time for temperature sweeping between impedance spect (min)
frequency = '007-3'         ###Minimum Frequency 007-3
Tamplitude = '010'           ##percentage of the amplitude
charNumber = 3              ###DO NOT CHANGE
offset = '+00'              ##offset with respect to room temperature
tempdir = os.path.join(path, "tsweep\\")   ## the dir for temp sweep data
if not os.path.exists(tempdir):
    os.mkdir(tempdir)

##Electrical Settings##
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

### Path and name where data are saved ####
temp_fsweep=0
temp = TemperatureBoard(port, baudRate)
temp.begin()
temp.setTemperature(temp.wave["pid"], IS_temperature)
time.sleep(60 * wait_time)
while True:
    scan=3 # sequential

    lockIn = MFIA(deviceID)
    now = datetime.datetime.now()
    lockIn.set2TerminalMode(amplitude, startFrequency, currentRange, demodRate, samplingRate)
    #  For temperatire to adjust time.sleep(20)
    print('Temperature:',temp.pollData(charNumber))
    ctime=now.strftime("%Y-%m-%d_%H%M")
    filename=str(amplitude)+'V_accuracy_'+str(accuracy)+'_scan_'+str(scan)+'_'+ctime
    print(filename)
    lockIn.setAmplitude(amplitude)
    lockIn.begin()
    reI_now=[]
    #     status = lockIn.sweeperStatus()
    ss=time.time()
    data=pd.DataFrame(data={
                "abs": [],
                "phs": [],
                "size": [],
                "frequency": []})
    for j in range(len(frequency_end)):
        print('frequency', frequency_end[-j-1],' to ',frequency_start[-j-1],', num of pt ', npoint[-j-1])
        lockIn.sweeperSet(frequency_start[-j-1], frequency_end[-j-1], npoint[-j-1], scan, accuracy=accuracy)
        lockIn.setFrequency( frequency_end[-j-1])
        autorange_current(deviceID,lockIn)
        time.sleep(5)
        print('autorange')

        lockIn.sweeperStart()
        status = lockIn.sweeperStatus()
        while not status['done']:
            print('not done')
            time.sleep(1)
            newdata=lockIn.sweeperRead()
            # if not data['nan']: print(data)
            status = lockIn.sweeperStatus()
        if len(newdata) == 0:
            print('no data')
        else:
            # data["temperature"] = temp.pollData(charNumber)
            data = data.append(pd.DataFrame(data=newdata), sort=False, ignore_index=True)

            print('temp:',temp.pollData(charNumber) )

        temp_fsweep=temp.pollData(charNumber)
        lockIn.sweeperClose()

    reI_now = np.array(data['x'].values)

    print('Finished one sweep,time ',time.time()-ss)
    print(data.head())

    data.to_csv(path+filename+'temp_'+str(temp_fsweep)+'.csv',sep='\t',index=False)
    # if i!=0:
    #     diff = np.abs(np.mean((reI_pre - reI_now) / reI_pre))
    #     reI_pre = reI_now
    #     print('\n\n\n difference is ',diff,'\n\n\n')        #
        # if diff<1:
    temp.disableOutput()
    print("Output Disabled")
    temp.end()
    # tempsweep(temperature_sweep_time,amplitude,subDirectoryData)
    constant_temperature(amplitude,subDirectoryData,Dehydrate_temperature,2,'log')
    temp = TemperatureBoard(port, baudRate)
    temp.begin()
    temp.setTemperature(temp.wave["pid"], IS_temperature)
    time.sleep(60*wait_time)
    #
    # else:
    #     reI_pre = reI_now
    #
    # # lockIn.adjustRange(10e-9)

    instant = lockIn.pollData()
    i+=1
def signal_handler(sig, frame):
    temp.disableOutput()
    print("Output Disabled")
    temp.end()


signal.signal(signal.SIGTERM, signal_handler)



# frequencies = np.logspace(np.log10(startFrequency), np.log10(endFrequency), num=samples)
# middlepoint=np.argmin(np.abs(frequencies-middleFrequency))
# frequency_start=[startFrequency,frequencies[middlepoint+1]]
# frequency_end=[frequencies[middlepoint],endFrequency]
# npoint=[middlepoint,len(frequencies)-middlepoint]

# section_number=3   ## how many different section do you want to do the sweep
# frequencies=np.logspace(np.log10(startFrequency), np.log10(endFrequency), num=samples)
# npoint=int(np.ceil(len(frequencies)/section_number))
# frequency_start=frequencies[::npoint]
# frequency_end=frequencies[npoint::npoint]
# frequency_end=np.append(frequency_end,endFrequency)
# print(frequency_start)

