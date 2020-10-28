from GUI_settings import SettingsGUI
from GUI_control import ControlGUI
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QComboBox, QFileDialog, QMessageBox, QToolTip, QApplication, QMainWindow
import sys
from CONSTANTS import CONSTANT

app = QtWidgets.QApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
else:
    print('QApplication instance already exists: %s' % str(app))

output = SettingsGUI()
app.exec_()
settings = output.output
output.close

window = ControlGUI(settings)
window.show()
app.exec_()
app.exit


