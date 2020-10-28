# To execute this script copy paste the following line:
# exec(open("C:\\Users\\vcostanz\\Desktop\\Pyhton Projects\\TemperatureBoard - v3.6\\Main_multicycles.py").read())
# after having modified the script according to your needs


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
import sys
sys.path.insert(0, 'C:\\Users\\vcostanz\\Desktop\\Linghui\\PYTHON\\MFIA_LH')
sys.path.append('C:\\Users\\vcostanz\\Desktop\\Linghui\\PYTHON\\TemperatureBoard_LH')
from MFIA import MFIA
from TemperatureBoard import TemperatureBoard
# import PyQt5
import datetime
import time
import pandas as pd
import numpy as np
def tempsweep(runtime,tempdir):
    port = 'COM5'
    baudRate = 1000000

    now = datetime.datetime.now()
    ctime = now.strftime("%Y-%m-%d_%H%M")

    ### Path and name where data are saved ####
    subDirectoryData =tempdir  #KEVIN\\[0] Test starts here\\Polymer2_PET\\20191021\\' #Folder where the data are saved

    deviceID = 'dev3275'
    amplitudeExct = 1e-2  ###Amplitude of the excitation sine in V
    frequencyExct = 200e0  # 500e2
    currentRange = 1e-6
    demodRate = 100e3  ###DO NOT CHANGE
    samplingRate = 0.001  ###DO NOT CHANGE

    ##Temperature Settings##
    frequency = '007-3'         ###Minimum Frequency 007-3
    amplitude = '010'           ##percentage of the amplitude
    temperature = '20.00'
    charNumber = 5              ###DO NOT CHANGE
    offset=0

    temp = TemperatureBoard(port, baudRate)
    temp.begin()

    fileIDData = 'pectin30CaCl2_'+str(amplitudeExct)+"V_"+str(frequencyExct)+'Hz_'+ctime

    lockIn = MFIA(deviceID)
    lockIn.set2TerminalMode(amplitudeExct, frequencyExct, currentRange, demodRate, samplingRate)
    lockIn.begin()

    data = lockIn.pollData()
    data["temperature"] = temp.pollData(charNumber)
    file = temp.selectFile(subDirectoryData, fileIDData)
    temp.writeDataToFile(file, data, True)
    # input("Press Enter to continue...")

    temp.setWave(temp.wave["sine"], frequency, amplitude,offset)

    initialtime=time.time()
    try:
        while time.time()-initialtime<60*runtime:
            start = time.time()
            data = lockIn.pollData()
            data["temperature"] = temp.pollData(charNumber)
            time.sleep(0.01)
            end = time.time()
            data["time"] = end
            temp.writeDataToFile(file, data)
        temp.closeFile(file)
        temp.disableOutput()
        print("Output Disabled")
        temp.end()
    except KeyboardInterrupt:
        temp.closeFile(file)
        temp.disableOutput()
        print("Output Disabled")
        temp.end()

