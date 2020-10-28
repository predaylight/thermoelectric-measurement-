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
# import sys
# sys.path.insert(0, 'C:\\Users\\vcostanz\\Desktop\\Linghui\\PYTHON\\MFIA_LH')
# # sys.path.append('C:\\Users\\vcostanz\\Desktop\\Linghui\\PYTHON\\TemperatureBoard_LH')
# sys.path.append('C:\\Users\\vcostanz\\Desktop\\Pyhton Projects\\TemperatureBoard')
#

from MFIA import MFIA
from TemperatureBoard import TemperatureBoard
# import PyQt5
import datetime
import time
import pandas as pd
import numpy as np
def tempsweep(runtime,amplitudeExct,subDirectoryData):
    # To execute this script copy paste the following line:
    # exec(open("C:\\Users\\vcostanz\\Desktop\\Pyhton Projects\\TemperatureBoard - v3.6\\Main.py").read())
    # after having modified the script according to your needs

    import sys
    sys.path.insert(0, 'C:\\Users\\vcostanz\\Desktop\\Linghui\\PYTHON\\MFIA_LH')
    sys.path.append('C:\\Users\\vcostanz\\Desktop\\Pyhton Projects\\TemperatureBoard')

    from TemperatureBoard import TemperatureBoard
    from MFIA_LH import MFIA
    import time

    from autorange_current import autorange_current
    port = 'COM5'
    baudRate = 1000000

    #### TODO: implement calibration reading ####
    subDirectoryCalibration = 'C:\\Users\\vcostanz\\Desktop\\'
    fileIDCalibration = 'test.txt'
    #############################################

    now = datetime.datetime.now()
    ctime = now.strftime("%Y-%m-%d_%H%M")
    frequency = '010-3'  ###Minimum Frequency 007-3
    amplitude = '020'  ##percentage of the amplitude
    offset = '+05'  ##offset with respect to room temperature
    temperature = '50.00'
    charNumber = 3  ###DO NOT CHANGE

    ##### Current Reading Settings #####
    deviceID = 'dev3275'
    frequencyExct = 200e0
    currentRange = 10e-6
    demodRate = 100e3  ###DO NOT CHANGE
    samplingRate = 0.001  ###DO NOT CHANGE

    temp = TemperatureBoard(port, baudRate)
    temp.begin()
    # temp.setTemperature(temp.wave["pid"], temperature)
    temp.setWave(temp.wave["sine"], frequency, amplitude, offset)
    fileIDData =  str(amplitudeExct) + "V_" + str(frequencyExct) + 'Hz_' + ctime

    lockIn = MFIA(deviceID)
    lockIn.set2TerminalMode(amplitudeExct, frequencyExct, currentRange, demodRate, samplingRate)
    lockIn.begin()
    autorange_current(deviceID, lockIn)

    data = lockIn.pollData()
    data["temperature"] = temp.pollData(charNumber)
    file = temp.selectFile(subDirectoryData, fileIDData)
    temp.writeDataToFile(file, data, True)
    initialtime = time.time()

    while time.time()-initialtime<60*runtime:
        start = time.time()
        data = lockIn.pollData()
        data["temperature"] = temp.pollData(charNumber)
        end = time.time()
        data["time"] = end - start
        temp.writeDataToFile(file, data)
        endGlobal = time.time()
        print('poll data')

    temp.disableOutput()  ###Uncomment this to switch the controller off
    print("Output Disabled")
    temp.end()

    # port = 'COM5'
    # baudRate = 1000000
    #
    # now = datetime.datetime.now()
    # ctime = now.strftime("%Y-%m-%d_%H%M")
    #
    # ### Path and name where data are saved ####
    #
    # deviceID = 'dev3275'
    # amplitudeExct = 1e-2  ###Amplitude of the excitation sine in V
    # frequencyExct = 200e0  # 500e2
    # currentRange = 1e-6
    # demodRate = 100e3  ###DO NOT CHANGE
    # samplingRate = 0.001  ###DO NOT CHANGE
    #
    # ##Temperature Settings##
    # frequency = '007-3'         ###Minimum Frequency 007-3
    # amplitude = '010'           ##percentage of the amplitude
    # temperature = '20.00'
    # charNumber = 5              ###DO NOT CHANGE
    #
    # temp = TemperatureBoard(port, baudRate)
    # temp.begin()
    # temp.setWave(temp.wave["sine"], frequency, amplitude)
    #
    # fileIDData = 'pectin30CaCl2_'+str(amplitudeExct)+"V_"+str(frequencyExct)+'Hz_'+ctime
    #
    # lockIn = MFIA(deviceID)
    # lockIn.set2TerminalMode(amplitudeExct, frequencyExct, currentRange, demodRate, samplingRate)
    # lockIn.begin()
    #
    # data = lockIn.pollData()
    # data["temperature"] = temp.pollData(charNumber)
    # file = temp.selectFile(subDirectoryData, fileIDData)
    # temp.writeDataToFile(file, data, True)
    # # input("Press Enter to continue...")
    # print(data)
    #
    # initialtime=time.time()
    # print(time.time()-initialtime)
    # while time.time()-initialtime<60*runtime:
    #     start = time.time()
    #     data = lockIn.pollData()
    #     data["temperature"] = temp.pollData(charNumber)
    #     print(data)
    #
    #     # time.sleep(0.01)
    #     end = time.time()
    #     data["time"] = end-start
    #     print('time')
    #     temp.writeDataToFile(file, data)
    #
    #
    # temp.closeFile(file)
    # temp.disableOutput()
    # print("Output Disabled")
    # temp.end()
