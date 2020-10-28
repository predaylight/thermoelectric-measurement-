from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QComboBox, QFileDialog, QMessageBox, QToolTip
from PyQt5.QtCore import *
import serial.tools.list_ports
import sys
from GUI_userProfile import UserProfile

class SettingsGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Settings')
        self.__app__ = {}

        self.__app__['excitationfrequency'] = {}
        self.__app__['excitationfrequency']['label'] = QtWidgets.QLabel('Excitation frequency: ')
        self.__app__['excitationfrequency']['value'] = QtWidgets.QLineEdit()
        self.__app__['excitationfrequency']['value'].setToolTip('Excitation Frequency of the DUT. <h3>Only numbers allowed</h3>')
        self.__app__['excitationfrequency']['value'].setText('100')
        self.__app__['excitationfrequency']['multiplier'] = QComboBox()
        self.__app__['excitationfrequency']['multiplier'].addItem('mHz')
        self.__app__['excitationfrequency']['multiplier'].addItem('Hz')
        self.__app__['excitationfrequency']['multiplier'].addItem('kHz')
        self.__app__['excitationfrequency']['multiplier'].addItem('MHz')
        self.__app__['excitationfrequency']['multiplier'].setCurrentIndex(1)

        self.__app__['excitationvoltage'] = {}
        self.__app__['excitationvoltage']['label'] = QtWidgets.QLabel('Excitation voltage: ')
        self.__app__['excitationvoltage']['value'] = QtWidgets.QLineEdit()
        self.__app__['excitationvoltage']['value'].setText('100')
        self.__app__['excitationvoltage']['value'].setToolTip('Excitation Voltage of the DUT. <h3>only numbers allowed)</h3>')
        self.__app__['excitationvoltage']['multiplier'] = QComboBox()
        self.__app__['excitationvoltage']['multiplier'].addItem('mV')
        self.__app__['excitationvoltage']['multiplier'].addItem('V')

        self.__app__['currentrange'] = {}
        self.__app__['currentrange']['label'] = QtWidgets.QLabel('Current Range: ')
        self.__app__['currentrange']['value'] = QComboBox()
        self.__app__['currentrange']['value'].setToolTip('Current Range for the Measurement <br><h3>(two orders of magnitude higher than the maximum read current)</h3>')
        self.__app__['currentrange']['value'].addItem('10 nA')
        self.__app__['currentrange']['value'].addItem('100 nA')
        self.__app__['currentrange']['value'].addItem('1 uA')
        self.__app__['currentrange']['value'].addItem('10 uA')
        self.__app__['currentrange']['value'].addItem('100 uA')
        self.__app__['currentrange']['value'].addItem('1 mA')
        self.__app__['currentrange']['value'].addItem('10 mA')
        self.__app__['currentrange']['value'].setCurrentIndex(4)

        self.__app__['temperature'] = {}
        self.__app__['temperature']['function'] = {}
        self.__app__['temperature']['function']['label'] = QtWidgets.QLabel('Temperature function: ')
        self.__app__['temperature']['function']['value'] = QComboBox()
        self.__app__['temperature']['function']['value'].addItem('Sine')
        self.__app__['temperature']['function']['value'].addItem('Triangle')
        self.__app__['temperature']['function']['value'].addItem('Reference')
        self.__app__['temperature']['function']['value'].setCurrentIndex(0)
        self.__app__['temperature']['function']['value'].activated.connect(self.adjustSettings)
        self.__app__['temperature']['function']['userprofile'] = QPushButton("User profile")
        self.__app__['temperature']['function']['userprofile'].clicked.connect(self.setTemperatureProfile)
        self.__app__['temperature']['reference'] = {}
        self.__app__['temperature']['reference']['label'] = QtWidgets.QLabel('Temperature °C: ')
        self.__app__['temperature']['reference']['value'] = QtWidgets.QLineEdit()

        self.__app__['temperature']['frequency'] = {}
        self.__app__['temperature']['frequency']['label'] = QtWidgets.QLabel('Frequency (min: 7mHz): ')
        self.__app__['temperature']['frequency']['value'] = QtWidgets.QLineEdit()
        self.__app__['temperature']['frequency']['multiplier'] = QComboBox()
        self.__app__['temperature']['frequency']['multiplier'].addItem("mHz")
        self.__app__['temperature']['frequency']['multiplier'].addItem("Hz")
        self.__app__['temperature']['frequency']['multiplier'].addItem("kHz")

        self.__app__['temperature']['amplitude'] = {}
        self.__app__['temperature']['amplitude']['label'] = QtWidgets.QLabel('Amplitude: ')
        self.__app__['temperature']['amplitude']['value'] = QtWidgets.QLineEdit()

        self.__app__['portcom'] = {}
        self.__app__['portcom']['label'] = QtWidgets.QLabel('COM Port: ')
        self.__app__['portcom']['value'] = QComboBox()
        portcom = serial.tools.list_ports.comports()
        for port in portcom:
            self.__app__['portcom']['value'].addItem(port.device)
        self.__app__['portcom']['value'].setCurrentIndex(1)

        self.__app__['filename'] = {}
        self.__app__['filename']['label'] = QtWidgets.QLabel('File name: ')
        self.__app__['filename']['value'] = QtWidgets.QLineEdit()
        self.__app__['filename']['value'].setText('data')

        self.__app__['filepath'] = {}
        self.__app__['filepath']['label'] = QtWidgets.QLabel('Save Path: ')
        self.__app__['filepath']['value'] = QtWidgets.QLineEdit()
        self.__app__['filepath']['button'] = QPushButton('Path')
        self.__app__['filepath']['button'].clicked.connect(self.selectDir)

        self.__app__["start"] = QPushButton('Start')
        self.__app__["start"].clicked.connect(self.start)

        layout = QGridLayout()
        self.layout = layout;

        layout.addWidget(self.__app__["excitationfrequency"]['label'], 0, 0)
        layout.addWidget(self.__app__['excitationfrequency']['value'], 0, 1)
        layout.addWidget(self.__app__['excitationfrequency']['multiplier'], 0, 2)

        layout.addWidget(self.__app__['excitationvoltage']['label'], 1, 0)
        layout.addWidget(self.__app__['excitationvoltage']['value'], 1, 1)
        layout.addWidget(self.__app__['excitationvoltage']['multiplier'], 1, 2)

        layout.addWidget(self.__app__['currentrange']['label'], 2, 0)
        layout.addWidget(self.__app__['currentrange']['value'], 2, 1)

        layout.addWidget(self.__app__['temperature']['function']['label'], 3, 0)
        layout.addWidget(self.__app__['temperature']['function']['value'], 3, 1)
        layout.addWidget(self.__app__['temperature']['function']['userprofile'], 3, 2)

        layout.addWidget(self.__app__['temperature']['frequency']['label'], 4, 0)
        layout.addWidget(self.__app__['temperature']['frequency']['value'], 4, 1)
        layout.addWidget(self.__app__['temperature']['frequency']['multiplier'], 4, 2)

        layout.addWidget(self.__app__['temperature']['reference']['label'], 4, 0)
        layout.addWidget(self.__app__['temperature']['reference']['value'], 4, 1)

        layout.addWidget(self.__app__['temperature']['amplitude']['label'], 5, 0)
        layout.addWidget(self.__app__['temperature']['amplitude']['value'], 5, 1)

        layout.addWidget(self.__app__['portcom']['label'], 6, 0)
        layout.addWidget(self.__app__['portcom']['value'], 6, 1)

        layout.addWidget(self.__app__['filename']['label'], 7, 0)
        layout.addWidget(self.__app__['filename']['value'], 7, 1)

        layout.addWidget(self.__app__['filepath']['label'], 8, 0)
        layout.addWidget(self.__app__['filepath']['value'], 8, 1)
        layout.addWidget(self.__app__['filepath']['button'], 8, 2)

        layout.addWidget(self.__app__["start"], 9, 1, 1, 1)

        ## DEFAULT SHOWN SETTINGS ##
        self.__app__['temperature']['frequency']['label'].show()
        self.__app__['temperature']['frequency']['value'].show()
        self.__app__['temperature']['frequency']['multiplier'].show()
        self.__app__['temperature']['amplitude']['label'].show()
        self.__app__['temperature']['amplitude']['value'].show()
        self.__app__['temperature']['reference']['label'].hide()
        self.__app__['temperature']['reference']['value'].hide()

        self.setLayout(layout)
        self.setWindowTitle('Settings')
        self.show()

    def selectDir(self):
        self.__app__["directory"] = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if self.__app__["directory"]:
            self.__app__['filepath']['value'].setText(self.__app__["directory"])

    def adjustSettings(self):
        if self.__app__['temperature']['function']['value'].currentText() == 'Reference':
            self.__app__['temperature']['frequency']['label'].hide()
            self.__app__['temperature']['frequency']['value'].hide()
            self.__app__['temperature']['frequency']['multiplier'].hide()
            self.__app__['temperature']['amplitude']['label'].hide()
            self.__app__['temperature']['amplitude']['value'].hide()
            self.__app__['temperature']['reference']['label'].show()
            self.__app__['temperature']['reference']['value'].show()
        else:
            self.__app__['temperature']['frequency']['label'].show()
            self.__app__['temperature']['frequency']['value'].show()
            self.__app__['temperature']['frequency']['multiplier'].show()
            self.__app__['temperature']['amplitude']['label'].show()
            self.__app__['temperature']['amplitude']['value'].show()
            self.__app__['temperature']['reference']['label'].hide()
            self.__app__['temperature']['reference']['value'].hide()

    def setTemperatureProfile(self):
        self.userProfile = UserProfile()


    def start(self):
        __output__ = {}
        flag = False
        if not self.__app__['excitationfrequency']['value'].text().isdigit():
            self.__errorDisplay__('Excitation Frequency Format', 'Only numbers allowed')
            flag = True
        else:
            __output__['excitationfrequency'] = {'frequency': self.__app__['excitationfrequency']['value'].text(),
                                                  'multiplier': self.__app__['excitationfrequency']['multiplier'].currentIndex()}
        if not self.__app__['excitationvoltage']['value'].text().isdigit():
            self.__errorDisplay__('Excitation Voltage Format', 'Only numbers allowed')
            flag = True
        else:
            __output__['excitationvoltage'] = {'voltage': self.__app__['excitationvoltage']['value'].text(),
                                                'multiplier': self.__app__['excitationvoltage']['multiplier'].currentIndex()}
        __output__['currentrange'] = self.__app__['currentrange']['value'].currentIndex()
        __output__['portcom'] = self.__app__['portcom']['value'].currentText()
        __output__['filename'] = self.__app__['filename']['value'].text()
        __output__['filepath'] = self.__app__['filepath']['value'].text()
        __output__['temperature'] = {'function': self.__app__['temperature']['function']['value'].currentIndex()}
        checkedreference = None
        checkedfrequency = None
        checkedamplitude = None
        if __output__['temperature']['function'] == 2:
            checkedreference = self.__checkInputReference__(self.__app__['temperature']['reference']['value'].text())
            if checkedreference['flag']:
                self.__errorDisplay__('Reference Temperature Format', 'Reference temperature must be a number (look at the hint for more info)')
            else:
                __output__['temperature']['reference'] = checkedreference['value']
        else:
            checkedfrequency = self.__checkInput__(self.__app__['temperature']['frequency']['value'].text())
            checkedamplitude = self.__checkInput__(self.__app__['temperature']['amplitude']['value'].text(), 100)
            if checkedfrequency['flag']:
                self.__errorDisplay__('Frequency Format', 'Frequency cannot have more than three digits')
            elif checkedamplitude['flag']:
                self.__errorDisplay__('Amplitude Format', 'Amplitude cannot have more than three digits')
            else:
                __output__['temperature']['frequency'] = checkedfrequency['value']
                __output__['temperature']['multiplier'] = self.__app__['temperature']['frequency']['multiplier'].currentIndex()
                __output__['temperature']['amplitude'] = checkedamplitude['value']
        if checkedreference is None:
            if checkedamplitude['flag'] or checkedfrequency['flag'] or flag:
                return
            else:
                self.output = self.__inputFormat__(__output__)
                self.close()
                QCoreApplication.quit()
        else:
            if checkedreference['flag'] or flag:
                return
            else:
                self.output = self.__inputFormat__(__output__)
                self.close()
                QCoreApplication.quit()

    def __checkInputReference__(self, input: str):
        data = input.split('.')
        for element in data:
            output = {'flag': len(element) > 2 or not element.isdigit()}
            if output['flag']:
                break
        if not output['flag']:
            output['value'] = input
            output['value'] = ''.join([input, '.00']) if len(data) == 1 and len(data[0]) == 2 else output['value']
            output['value'] = ''.join(['0', input, '.00']) if len(data) == 1 and data[0] == 1 else output['value']
            if len(data) == 2:
                output['value'] = input
                output['value'] = ''.join(['0', output['value']]) if len(data[0]) == 1 else output['value']
                output['value'] = ''.join([output['value'], '0']) if len(data[1]) == 1 else output['value']
        else:
            output['value'] = 'nan'
        return output

    def __checkInput__(self, input: str, maxinput = None):
        output = {'flag': len(input) > 3 or not input.isdigit()}
        if maxinput is not None and not output['flag']:
            output['flag'] = int(input) > maxinput
        if output['flag']:
            output['value'] = 'nan'
        else:
            output['value'] = ''.join(['00', input]) if len(input) == 1 else input
            output['value'] = ''.join(['0', input]) if len(input) == 2 else output['value']
        return output

    def __errorDisplay__(self, title: str,msg: str):
        QMessageBox.about(self, title, msg)

    def __inputFormat__(self, input):
        output = {'settings': None,
                  'excitation': None,
                  'temperature': None}
        output['settings'] = {'portcom': input['portcom'],
                  'filename': input['filename'],
                  'filepath': input['filepath']}
        output['excitation'] = {'voltage': float(input['excitationvoltage']['voltage']),
                                'frequency': int(input['excitationfrequency']['frequency']),
                                'range': 0}
        output['excitation']['voltage'] = output['excitation']['voltage'] if input['excitationvoltage']['multiplier'] == 1 else output['excitation']['voltage']*1e-3

        if input['excitationfrequency']['multiplier'] == 0: output['excitation']['frequency'] = output['excitation']['frequency']*1e-3
        elif input['excitationfrequency']['multiplier'] == 2: output['excitation']['frequency'] = output['excitation']['frequency']*1e3
        elif input['excitationfrequency']['multiplier'] == 3: output['excitation']['frequency'] = output['excitation']['frequency']*1e6
        else: None

        if input['currentrange'] == 0: output['excitation']['range'] = 10e-9
        elif input['currentrange'] == 1: output['excitation']['range'] = 100e-9
        elif input['currentrange'] == 2: output['excitation']['range'] = 1e-6
        elif input['currentrange'] == 3: output['excitation']['range'] = 10e-6
        elif input['currentrange'] == 4: output['excitation']['range'] = 100e-6
        elif input['currentrange'] == 5: output['excitation']['range'] = 1e-3
        elif input['currentrange'] == 6: output['excitation']['range'] = 10e-3
        else: None

        output['temperature'] = {'function': input['temperature']['function']}
        if output['temperature']['function'] != 2:
            output['temperature']['amplitude'] = input['temperature']['amplitude']
            if input['temperature']['multiplier'] == 0: output['temperature']['frequency'] = input['temperature']['frequency']+'-3'
            elif input['temperature']['multiplier'] == 1: output['temperature']['frequency'] = input['temperature']['frequency']+'+0'
            elif input['temperature']['multiplier'] == 2: output['temperature']['frequency'] = input['temperature']['frequency'] + '+3'
        else:
            output['temperature']['reference'] = input['temperature']['reference']
        return output

def run():

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    else:
        print('QApplication instance already exists: %s' % str(app))

    setting = SettingsGUI()
    app.exec_()
    app.exit()


# this is good practice as well, it allows your code to be imported without executing
if __name__ == '__main__':  # then this script is being run directly,
    run()
else:  # this script is being imported
    ...  # usually you can leave off the else