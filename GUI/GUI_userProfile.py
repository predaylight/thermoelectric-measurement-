from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QComboBox, QFileDialog, QMessageBox, QToolTip, QTableWidget
from PyQt5.QtCore import *
import sys

class UserProfile(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.output = {}
        self.__app__ = {}

        self.__app__['label'] = {}
        self.__app__['label']['function'] = QtWidgets.QLabel('Function')
        self.__app__['label']['reference'] = QtWidgets.QLabel('Temperature')
        self.__app__['label']['amplitude'] = QtWidgets.QLabel('Amplitude')
        self.__app__['label']['frequency'] = QtWidgets.QLabel('Frequency')
        self.__app__['label']['time'] = QtWidgets.QLabel('Time (min)')

        self.__app__['value'] = {}
        self.__app__['value']['function'] = QComboBox()
        self.__app__['value']['function'].addItem('Sine')
        self.__app__['value']['function'].addItem('Triangle')
        self.__app__['value']['function'].addItem('Reference')
        self.__app__['value']['function'].setCurrentIndex(0)
        self.__app__['value']['function'].activated.connect(self.adjustSettings)

        self.__app__['value']['reference'] = QtWidgets.QLineEdit()
        self.__app__['value']['amplitude'] = QtWidgets.QLineEdit()
        self.__app__['value']['frequency'] = QtWidgets.QLineEdit()
        self.__app__['value']['multiplier'] = QComboBox()
        self.__app__['value']['multiplier'].addItem('mHz')
        self.__app__['value']['multiplier'].addItem('Hz')
        self.__app__['value']['multiplier'].addItem('kHz')
        self.__app__['value']['multiplier'].setCurrentIndex(0)
        self.__app__['value']['time'] = QtWidgets.QLineEdit()

        self.__app__['add'] = QPushButton('Add')
        self.__app__['add'].clicked.connect(self.addRow)

        self.__app__['table'] = QTableWidget(self)
        self.__app__['table'].setColumnCount(6)

        self.__app__['done'] = QPushButton('Done')
        self.__app__['done'].clicked.connect(self.done)

        layout = QGridLayout()
        self.layout = layout;

        layout.addWidget(self.__app__['label']['function'], 0, 0)
        layout.addWidget(self.__app__['label']['reference'], 0, 1)
        layout.addWidget(self.__app__['label']['amplitude'], 0, 1)
        layout.addWidget(self.__app__['label']['frequency'], 0, 2)
        layout.addWidget(self.__app__['label']['time'], 0, 4)

        layout.addWidget(self.__app__['value']['function'], 1, 0)
        layout.addWidget(self.__app__['value']['reference'], 1, 1, 1, 1)
        layout.addWidget(self.__app__['value']['amplitude'], 1, 1)
        layout.addWidget(self.__app__['value']['frequency'], 1, 2)
        layout.addWidget(self.__app__['value']['multiplier'], 1, 3)
        layout.addWidget(self.__app__['value']['time'], 1, 4, 1, 1)
        layout.addWidget(self.__app__['add'], 1, 5)

        layout.addWidget(self.__app__['table'], 2, 0, 5, 6)
        layout.addWidget(self.__app__['done'], 7, 2, 1, 2)


        ## DEFAULT SHOWN SETTINGS ##
        self.__app__['label']['amplitude'].show()
        self.__app__['label']['frequency'].show()
        self.__app__['label']['reference'].hide()
        self.__app__['value']['reference'].hide()

        self.setLayout(layout)
        self.setWindowTitle('User Profile')
        self.show()

    def adjustSettings(self):
        if self.__app__['value']['function'].currentIndex() != 2:
            self.__app__['label']['reference'].hide()
            self.__app__['label']['amplitude'].show()
            self.__app__['label']['frequency'].show()
            self.__app__['value']['reference'].hide()
            self.__app__['value']['reference'].setText('')
            self.__app__['value']['amplitude'].show()
            self.__app__['value']['frequency'].show()
            self.__app__['value']['multiplier'].show()

        else:
            self.__app__['label']['amplitude'].hide()
            self.__app__['label']['frequency'].hide()
            self.__app__['label']['reference'].show()
            self.__app__['value']['amplitude'].hide()
            self.__app__['value']['amplitude'].setText('')
            self.__app__['value']['frequency'].hide()
            self.__app__['value']['frequency'].setText('')
            self.__app__['value']['multiplier'].hide()
            self.__app__['value']['reference'].show()

    def addRow(self):
        row = self.__app__['table'].rowCount()
        self.__app__['table'].insertRow(row)
        i = 0
        for keys in self.__app__['value']:
            if keys in ('multiplier', 'function'):
                text = self.__app__['value'][keys].currentText()
                if keys == 'multiplier':
                    text = '' if self.__app__['value']['function'].currentIndex() == 2 else self.__app__['value'][keys].currentText()
            else:
                text = self.__app__['value'][keys].text()
            self.__app__['table'].setItem(row, i, QtWidgets.QTableWidgetItem(text))
            i += 1


    def done(self):
        self.output = self.formatOutput()
        self.close()
        # QCoreApplication.quit()

    def formatOutput(self):
        output = {'function': [],
                  'reference': [],
                  'amplitude': [],
                  'frequency': [],
                  'multiplier': [],
                  'time': []}
        for row in range(self.__app__['table'].rowCount()):
            output['function'].append(self.__app__['table'].item(row,0).text())
            output['reference'].append(self.__app__['table'].item(row, 1).text())
            output['amplitude'].append(self.__app__['table'].item(row, 2).text())
            output['frequency'].append(self.__app__['table'].item(row, 3).text())
            output['multiplier'].append(self.__app__['table'].item(row, 4).text())
            output['time'].append(self.__app__['table'].item(row, 5).text())
        return output


def run():

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    else:
        print('QApplication instance already exists: %s' % str(app))

    window = UserProfile()
    app.exec_()
    app.exit()


if __name__ == '__main__':  # then this script is being run directly,
    run()
else:  # this script is being imported
    ...  # usually you can leave off the else