# To execute this script copy paste the following line in the Python Console:
# exec(open("C:\\Users\\vcostanz\\Desktop\\Linghui\\python\\temp_control.py").read())
# # after having modified the script according to your needs

import sys
sys.path.append('C:\\Users\\vcostanz\\Desktop\\Pyhton Projects\\TemperatureBoard')
sys.path.append('C:\\Users\\vcostanz\\Desktop\\Pyhton Projects\\MFIA')
from TemperatureBoard import TemperatureBoard
from MFIA import MFIA
import time
import signal


# print('Press Ctrl+C')
# # signal.pause()

# import PyQt5
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QPushButton, QVBoxLayout,QGridLayout,QComboBox,QFileDialog,QTableWidget
# import setting_gui
#
# app = QtWidgets.QApplication.instance()
# if app is None:
#     app = QtWidgets.QApplication(sys.argv)
# else:
#     print('QApplication instance already exists: %s' % str(app))
#
# setting = Settings()
# app.exec_()
# app.exit()



port = 'COM5'
baudRate = 1000000

#### TODO: implement calibration reading ####
subDirectoryCalibration = 'C:\\Users\\vcostanz\\Desktop\\'
fileIDCalibration = 'test.txt'
#############################################


### Path and name where data are saved ####
# subDirectoryData ='C:\\Users\\vcostanz\\Desktop\\Vinnie'                                        ##Folder where the data are saved
# fileIDData = 'test'
subDirectoryData ='C:\\Users\\vcostanz\\Desktop\\Linghui\\Silk_P3A' #Folder where the data are saved
fileIDData = '30C'

##Temperature Settings##
frequency = '010-3'         ###Minimum Frequency 007-3
amplitude = '005'           ##percentage of the amplitude
offset = '+00'              ##offset with respect to room temperature
temperature = '30.00'
charNumber = 5              ###DO NOT CHANGE


##### Current Reading Settings #####
deviceID = 'dev3275'
amplitudeExct = 1         ###Amplitude of the excitation sine in V
frequencyExct = 200e0
currentRange = 1e-3
demodRate = 100e3           ###DO NOT CHANGE
samplingRate = 0.001        ###DO NOT CHANGE


temp = TemperatureBoard(port, baudRate)
temp.begin()
temp.setTemperature(temp.wave["pid"], temperature)                  #use for constant temperature only (PID controller). Comment if you use the sine
# temp.setWave(temp.wave["sine"], frequency, amplitude, offset)     #use for sine changing temperature. Comment if you use the PID

# Automatically disable port when pressing ctrl-c
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    temp.disableOutput()
    print("Output Disabled")
    temp.end()

signal.signal(signal.SIGINT, signal_handler)
data={'time':[],
      'frequency': [],
                    'abs': [],
                    'phs': [],
                    'size': [],
                    'frequency': [],
                    'temperature':[]}
data["temperature"] = temp.pollData(charNumber)
file = temp.selectFile(subDirectoryData, fileIDData)
temp.writeDataToFile(file, data, True)
input("Press Enter to continue...")

while True:
    start = time.time()
    data["temperature"] = temp.pollData(charNumber)
    end = time.time()
    data["time"] = end - start
    temp.writeDataToFile(file, data)
    endGlobal = time.time()

temp.disableOutput()
temp.end()