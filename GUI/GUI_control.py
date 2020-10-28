import sys
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QComboBox, QFileDialog, QMessageBox, QToolTip, QApplication, QMainWindow
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtGui import QIcon

sys.path.append('C:\\Users\\vcostanz\\Desktop\\Pyhton Projects\\TemperatureBoard')
sys.path.append('C:\\Users\\vcostanz\\Desktop\\Pyhton Projects\\MFIA')
from TemperatureBoard import TemperatureBoard
from MFIA import MFIA

class ControlAndAcquisition(QObject):

    def __init__(self):
        super(ControlAndAcquisition, self).__init__()
        self.working = True                                         # this is our flag to control our loop

    def initHardware (self, settings):
        deviceID = 'dev3275'
        samplingRate = 0.001
        demodRate = 100e3
        baudRate = 1000000
        self.settings = settings
        self.charNumber = 5
        self.lockIn = MFIA(deviceID)
        self.lockIn.set2TerminalMode(settings['excitation']['voltage'],
                                     settings['excitation']['frequency'],
                                     settings['excitation']['range'],
                                     demodRate, samplingRate)
        self.lockIn.begin()
        self.temperature = TemperatureBoard(settings['settings']['portcom'], baudRate)
        self.temperature.begin()
        data = self.lockIn.pollData()
        data["temperature"] = self.temperature.pollData(self.charNumber)
        self.file = self.temperature.selectFile(settings['settings']['filepath'], settings['settings']['filename'])
        self.temperature.writeDataToFile(self.file, data, True)

    def work(self):
        if self.settings['temperature']['function'] == 0: self.temperature.setWave(self.temperature.wave["sine"],
                                                                                   self.settings['temperature']['frequency'],
                                                                                   self.settings['temperature']['amplitude'])
        elif self.settings['temperature']['function'] == 1: self.temperature.setWave(self.temperature.wave["triangle"],
                                                                                   self.settings['temperature']['frequency'],
                                                                                   self.settings['temperature']['amplitude'])
        elif self.settings['temperature']['function'] == 2: self.temperature.setTemperature(self.temperature.wave["pid"],
                                                                                            self.settings['temperature']['reference'])
        self.busyPolling = False
        self.busySetting = False
        while self.working:
            start = time.time()
            while self.busySetting: None
            data = self.lockIn.pollData()
            self.busyPolling = True
            data["temperature"] = self.temperature.pollData(self.charNumber)
            self.busyPolling = False
            end = time.time()
            data["time"] = end - start
            self.temperature.writeDataToFile(self.file, data)
        self.temperature.disableOutput()
        self.temperature.end()
        self.temperature.closeFile(self.file)
        self.close()
        # QCoreApplication.quit()

    def changeVoltage(self, amplitude):
        self.lockIn.setAmplitude(amplitude)

    def changeFrequency(self, frequency):
        self.lockIn.setFrequency(frequency)

    def adjustRange(self, index):
        if index == 0: self.lockIn.adjustRange(10e-9)
        elif index == 1: self.lockIn.adjustRange(100e-9)
        elif index == 2: self.lockIn.adjustRange(1e-6)
        elif index == 3: self.lockIn.adjustRange(10e-6)
        elif index == 4: self.lockIn.adjustRange(100e-6)
        elif index == 5: self.lockIn.adjustRange(1e-3)
        elif index == 6: self.lockIn.adjustRange(10e-3)
        elif index == 7: self.lockIn.autoRange()

    def changeTemperature(self, temperature):
        while self.busyPolling: None
        self.busySetting = True
        self.temperature.setTemperature(self.temperature.wave["pid"], str(temperature))
        self.busySetting = False

    def changeAmplitude(self, amplitude):
        if self.settings['temperature']['function'] == 0:
            self.temperature.setWave(self.temperature.wave["sine"], self.settings['temperature']['frequency'], amplitude)
        elif self.settings['temperature']['function'] == 1:
            self.temperature.setWave(self.temperature.wave["triangle"], self.settings['temperature']['frequency'], amplitude)


class ControlGUI(QWidget):

    def __init__(self, settings):
        super(ControlGUI, self).__init__()
        self.initUI(settings)
        self.loop(settings)

    def initUI(self, settings):

        self.setWindowTitle('Settings')
        self.__app__ = {}
        self.__app__['excitationfrequency'] = {}
        self.__app__['excitationfrequency']['label'] = QtWidgets.QLabel('Excitation frequency: ')
        self.__app__['excitationfrequency']['value'] = QtWidgets.QLineEdit()
        self.__app__['excitationfrequency']['value'].setText(str(settings['excitation']['frequency']))
        self.__app__['excitationfrequency']['value'].setToolTip(
            'Excitation Frequency of the DUT. <h3>Only numbers allowed</h3>')
        self.__app__['excitationfrequency']['value'].returnPressed.connect(self.__changeFrequency__)

        self.__app__['excitationvoltage'] = {}
        self.__app__['excitationvoltage']['label'] = QtWidgets.QLabel('Excitation voltage: ')
        self.__app__['excitationvoltage']['value'] = QtWidgets.QLineEdit()
        self.__app__['excitationvoltage']['value'].setText(str(settings['excitation']['voltage']))
        self.__app__['excitationvoltage']['value'].returnPressed.connect(self.__changeVoltage__)

        self.__app__['currentrange'] = {}
        self.__app__['currentrange']['label'] = QtWidgets.QLabel('Current Range: ')
        self.__app__['currentrange']['value'] = QComboBox()
        self.__app__['currentrange']['value'].setToolTip(
            'Current Range for the Measurement <br><h3>(two orders of magnitude higher than the maximum read current)</h3>')
        self.__app__['currentrange']['value'].addItem('10 nA')
        self.__app__['currentrange']['value'].addItem('100 nA')
        self.__app__['currentrange']['value'].addItem('1 uA')
        self.__app__['currentrange']['value'].addItem('10 uA')
        self.__app__['currentrange']['value'].addItem('100 uA')
        self.__app__['currentrange']['value'].addItem('1 mA')
        self.__app__['currentrange']['value'].addItem('10 mA')
        self.__app__['currentrange']['value'].addItem('auto')
        if settings['excitation']['voltage'] == 10e-9: self.__app__['currentrange']['value'].setCurrentIndex(0)
        elif settings['excitation']['voltage'] == 100e-9: self.__app__['currentrange']['value'].setCurrentIndex(1)
        elif settings['excitation']['voltage'] == 1e-6: self.__app__['currentrange']['value'].setCurrentIndex(2)
        elif settings['excitation']['voltage'] == 10e-6: self.__app__['currentrange']['value'].setCurrentIndex(3)
        elif settings['excitation']['voltage'] == 100e-6: self.__app__['currentrange']['value'].setCurrentIndex(4)
        elif settings['excitation']['voltage'] == 1e-3: self.__app__['currentrange']['value'].setCurrentIndex(5)
        elif settings['excitation']['voltage'] == 10e-3: self.__app__['currentrange']['value'].setCurrentIndex(6)
        self.__app__['currentrange']['value'].activated.connect(self.__adjustRange__)

        self.__app__['temperature'] = {}
        self.__app__['temperature']['reference'] = {}
        self.__app__['temperature']['reference']['label'] = QtWidgets.QLabel('Temperature °C: ')
        self.__app__['temperature']['reference']['value'] = QtWidgets.QLineEdit()
        if settings['temperature']['function'] == 2: self.__app__['temperature']['reference']['value'].setText(str(settings['temperature']['reference']))
        self.__app__['temperature']['reference']['value'].returnPressed.connect(self.__changeTemperature__)

        self.__app__['temperature']['amplitude'] = {}
        self.__app__['temperature']['amplitude']['label'] = QtWidgets.QLabel('Amplitude: ')
        self.__app__['temperature']['amplitude']['value'] = QtWidgets.QLineEdit()
        if settings['temperature']['function'] != 2: self.__app__['temperature']['amplitude']['value'].setText(str(settings['temperature']['amplitude']))
        self.__app__['temperature']['amplitude']['value'].returnPressed.connect(self.__changeAmplitude__)

        self.__app__['stop'] = QPushButton('Stop')

        layout = QGridLayout()

        layout.addWidget(self.__app__["excitationfrequency"]['label'], 0, 0)
        layout.addWidget(self.__app__['excitationfrequency']['value'], 0, 1)

        layout.addWidget(self.__app__['excitationvoltage']['label'], 1, 0)
        layout.addWidget(self.__app__['excitationvoltage']['value'], 1, 1)

        layout.addWidget(self.__app__['currentrange']['label'], 2, 0)
        layout.addWidget(self.__app__['currentrange']['value'], 2, 1)

        layout.addWidget(self.__app__['temperature']['reference']['label'], 3, 0)
        layout.addWidget(self.__app__['temperature']['reference']['value'], 3, 1)

        layout.addWidget(self.__app__['temperature']['amplitude']['label'], 3, 0)
        layout.addWidget(self.__app__['temperature']['amplitude']['value'], 3, 1)

        layout.addWidget(self.__app__['stop'], 4, 1, 1, 1)

        self.setLayout(layout)
        self.show()
        if settings['temperature']['function'] == 2:
            self.__app__['temperature']['reference']['label'].show()
            self.__app__['temperature']['reference']['value'].show()
            self.__app__['temperature']['amplitude']['label'].hide()
            self.__app__['temperature']['amplitude']['value'].hide()
        else:
            self.__app__['temperature']['reference']['label'].hide()
            self.__app__['temperature']['reference']['value'].hide()
            self.__app__['temperature']['amplitude']['label'].show()
            self.__app__['temperature']['amplitude']['value'].show()


        self.thread = None
        self.acquisitionAndcontrol = None


    def loop(self, settings):
        self.thread = QThread()  # a new thread to run our background tasks in
        self.acquisitionAndcontrol = ControlAndAcquisition()
        self.acquisitionAndcontrol.initHardware(settings)
        self.acquisitionAndcontrol.moveToThread(self.thread)
        self.thread.started.connect(self.acquisitionAndcontrol.work)

        self.__app__['stop'].clicked.connect(self.__stop__)
        self.thread.start()

    def __changeVoltage__(self):
        try:
            self.acquisitionAndcontrol.changeVoltage(float((self.__app__['excitationvoltage']['value'].text())))
        except ValueError:
            self.__errorDisplay__('Excitation Voltage Format', 'Only numbers allowed')

    def __changeFrequency__(self):
        try:
            self.acquisitionAndcontrol.changeFrequency(float((self.__app__['excitationfrequency']['value'].text())))
        except ValueError:
            self.__errorDisplay__('Excitation Frequency Format', 'Only numbers allowed')

    def __adjustRange__(self):
        index = self.__app__['currentrange']['value'].currentIndex()
        self.acquisitionAndcontrol.adjustRange(index)

    def __changeTemperature__(self):
        temperature = self.__app__['temperature']['reference']['value'].text()
        self.acquisitionAndcontrol.changeTemperature(temperature)

    def __changeAmplitude__(self):
        amplitude = self.__app__['temperature']['amplitude']['value'].text()
        self.acquisitionAndcontrol.changeAmplitude(amplitude)

    def __stop__(self):
        print("stop")
        self.acquisitionAndcontrol.working = False



    def __errorDisplay__(self, title: str,msg: str):
        QMessageBox.about(self, title, msg)


def run():


    app = QApplication(sys.argv)
    window = ControlGUI()
    window.show()
    sys.exit(app.exec_())

# this is good practice as well, it allows your code to be imported without executing
if __name__ == '__main__':  # then this script is being run directly,
    run()
else:  # this script is being imported
    ...  # usually you can leave off the else