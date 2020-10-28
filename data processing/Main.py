## Things need to implement:
# 1. when save the table, save also the cycle number, so that we could plot just single cycle

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QPushButton, QVBoxLayout,QGridLayout,QComboBox,QFileDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
import math
import pandas as pd
import numpy as np
import pandas as pd
import scipy
import glob
import os
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d
from bokeh.core.properties import field,value
from bokeh.models import ColumnDataSource, OpenURL, TapTool,LinearAxis,Range1d,HoverTool,CustomJS,Whisker,LabelSet
from bokeh.plotting import figure, output_file, show,curdoc
from bokeh.palettes import viridis,d3
from bokeh.models.widgets import *
from bokeh.layouts import *
from bokeh.models.arrow_heads import *
from bokeh.io import export_svgs
from errorbar import errorbar
try:
    from skimage.restoration import denoise_tv_chambolle
except ImportError:
    # skimage < 0.12
    from skimage.filters import denoise_tv_chambolle
from split_step2 import split_step2

class Ui_setting(QWidget):
    def setupUi(self, setting):
        self.dir_name='/Users/lwang/Desktop/OneDrive - California Institute of Technology/Research PhD/AC measurement/parylene_coating/Cu_pectin_no coat/*.txt'
        setting.setObjectName("setting")
        setting.resize(635, 300)
        self.centralWidget = QtWidgets.QWidget(setting)
        self.centralWidget.setObjectName("centralWidget")
        # self.pushButton_3.clicked.connect(self.add_plot)

        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 20, 121, 32))
        self.pushButton.setText("path")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.select_dir)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 50, 121, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText('plot')
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.ac_plot)

        self.label_7 = QtWidgets.QLabel(self.centralWidget)
        self.label_7.setGeometry(QtCore.QRect(30, 20, 121, 16))
        self.label_7.setText("Folder Path")

        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(QtCore.QRect(100, 20, 231, 20))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setText(self.dir_name)

        self.text_datares = QtWidgets.QTextEdit(self.centralWidget)
        self.text_datares.setGeometry(QtCore.QRect(200, 50, 100, 20))
        self.text_datares.setObjectName("text_datares")
        self.text_datares.setText('100')
        self.label_datares = QtWidgets.QLabel(self.centralWidget)
        self.label_datares.setGeometry(QtCore.QRect(30, 50, 121, 16))
        self.label_datares.setText("Ploting resolution")


        self.text_steprec = QtWidgets.QTextEdit(self.centralWidget)
        self.text_steprec.setGeometry(QtCore.QRect(200, 70, 100, 20))
        self.text_steprec.setObjectName("text_datares")
        self.text_steprec.setText('0.01')
        self.label_steprec = QtWidgets.QLabel(self.centralWidget)
        self.label_steprec.setGeometry(QtCore.QRect(30, 70, 121, 16))
        self.label_steprec.setText("diff(T) at T jump")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 90, 491, 501))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")

        self.plottype_area = QtWidgets.QScrollArea(self.gridLayoutWidget)
        self.plottype_area.setWidgetResizable(True)
        self.plottype_area.setObjectName("plottype_area")
        self.plottype_area.setGeometry(QtCore.QRect(0, 20, 400, 200))
        self.plottype_area.setObjectName("plottype_area")

        self.checkBox = QtWidgets.QCheckBox(self.plottype_area)
        self.checkBox.setGeometry(QtCore.QRect(10, 30, 200, 20))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setText("Amplitude vs time")

        self.checkBox_2 = QtWidgets.QCheckBox(self.plottype_area)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 50, 200, 20))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.setText("Phase vs time")

        self.checkBox_3 = QtWidgets.QCheckBox(self.plottype_area)
        self.checkBox_3.setGeometry(QtCore.QRect(10, 90, 200, 20))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.setText("Step_recognition_check")

        self.checkBox_4 = QtWidgets.QCheckBox(self.plottype_area)
        self.checkBox_4.setGeometry(QtCore.QRect(10, 110, 200, 20))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_4.setText("Response vs Temperature")

        self.checkBox_5 = QtWidgets.QCheckBox(self.plottype_area)
        self.checkBox_5.setGeometry(QtCore.QRect(10, 70, 200, 20))
        self.checkBox_5.setObjectName("checkBox_4")
        self.checkBox_5.setText("Temperature vs time")

        setting.setCentralWidget(self.centralWidget)
        QtCore.QMetaObject.connectSlotsByName(setting)

    def select_dir(self):
        self.dir_name = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.dir_name=self.dir_name+'/*.txt'
        if self.dir_name:
            self.textEdit.setText(self.dir_name)

    def exit(self):
        self.close()
        app.exec_()
    def ac_plot(self):
        # path='/Users/lwang/Desktop/OneDrive - California Institute of Technology/Research PhD/AC measurement/parylene_coating/Cu_pectin_no coat'
        path=self.textEdit.toPlainText()
        plotfrequency=int(self.text_datares.toPlainText())
        difft=float(self.text_steprec.toPlainText())
        pd.set_option('display.max_columns', None)
        pd.set_option('display.float_format', '{:.6g}'.format)
        tablecolumn=['filenames','time_sum','abs','temperature','phs']
        table=pd.DataFrame(columns=tablecolumn)
        i=0
        s1=figure(plot_width=1500, plot_height=400,tools="tap,crosshair,pan,reset,save,wheel_zoom,box_zoom",sizing_mode="stretch_both",output_backend="webgl")
        s2=figure(plot_width=1500, plot_height=400,tools="tap,crosshair,pan,reset,save,wheel_zoom,box_zoom",sizing_mode="stretch_both",output_backend="webgl")
        s3=figure(plot_width=1500, plot_height=400,tools="tap,crosshair,pan,reset,save,wheel_zoom,box_zoom",sizing_mode="stretch_both",output_backend="webgl")
        s4=figure(plot_width=1500, plot_height=400,tools="tap,crosshair,pan,reset,save,wheel_zoom,box_zoom",sizing_mode="stretch_both",output_backend="webgl")
        s5=figure(plot_width=1500, plot_height=400,tools="tap,crosshair,pan,reset,save,wheel_zoom,box_zoom",sizing_mode="stretch_both",output_backend="webgl")

        whatplot=[]
        if self.checkBox.isChecked():
            whatplot.append(s1)
        if self.checkBox_2.isChecked():
            whatplot.append(s2)
        if self.checkBox_3.isChecked():
            whatplot.append(s3)
        if self.checkBox_4.isChecked():
            whatplot.append(s4)
        if self.checkBox_5.isChecked():
            whatplot.append(s5)
        filenumber=len(glob.glob(path))
        colornumber=filenumber
        if filenumber<3:
            cmap=d3['Category20'][3]#len(glob.glob(path))]#
            colornumber=3
        elif filenumber<20:
            cmap=d3['Category20'][len(glob.glob(path))]
        else:
            print('Please have less than 20 files in the folder to plot')
            sys.exit()


        for name in glob.glob(path):
        #for name in glob.glob(os.path.join(path, '*.csv')):
            data=pd.read_csv(name,sep='\t',header=0)
            data['time_sum']=data['time'].cumsum()
            tname=name.split('/')[-1]
            tname=tname.split('.')[0]
            data['filenames']=tname
            print(tname)
            abs=np.array(data['abs'].tolist())
            absavg=np.mean(abs)
            rmse=np.sum(np.abs(abs-absavg)/(len(abs)-1))
            tf=np.abs(abs-absavg)<4*rmse
            data=data[tf]

            abs=np.array(data['abs'].tolist())
            temperature=np.array(data['temperature'].tolist())
            time_sum=np.array(data['time_sum'].tolist())
            phase=np.array(data['phs'].tolist())

            if (not self.checkBox_3.isChecked()) and (not self.checkBox_4.isChecked()):
                s1.line(x=time_sum[::plotfrequency],y=abs[::plotfrequency],color=cmap[i],legend=tname)
                s2.line(x=time_sum[::plotfrequency],y=phase[::plotfrequency],color=cmap[i],legend=tname)
                s5.line(x=time_sum[::plotfrequency], y=temperature[::plotfrequency],color=cmap[i],legend=tname)
                print('Not')
                i+=1
            else:
                denot=denoise_tv_chambolle(temperature,weight=0.4)
                diff=np.diff(denot)
                newdata,response,index2=split_step2(temperature,abs,phase,time_sum,100,25,difft)   # the last number is the current at that temperature you want to normalized by
                newdata['color']=cmap[i]
                newdata['legend']=tname
                newplotdata=newdata.loc[::plotfrequency,:].copy()
                np.set_printoptions(threshold=np.nan)
                source=ColumnDataSource(data=newplotdata)
                response['legend_amplitude']="Amplitude: "+tname
                response['legend_phase']="Phase: "+tname
                response['legend']=tname
                responsesource=ColumnDataSource(data=response)
                s1.line(x=time_sum[::plotfrequency],y=abs[::plotfrequency],color=cmap[i],legend=tname)
                s2.line(x=time_sum[::plotfrequency],y=phase[::plotfrequency],color=cmap[i],legend=tname)
                s5.line(x=time_sum[::plotfrequency],y=temperature[::plotfrequency],color=cmap[i],legend=tname)

                s3.line(x=time_sum[::plotfrequency], y=temperature[::plotfrequency],color='#f5d848',legend=tname)
                s3.multi_line(xs='time_sum', ys='temperature',source=source,color= cmap[i],legend=tname+'_data for response')
                s3.circle(x='time_cyclestart',y='T_cyclestart',source=responsesource,color='#FF0000',legend=tname+'_cycle start point')

                s4.yaxis.axis_label='Amplitude Response'
                s4.circle(x='Cycle_number',y='I_response',source=responsesource,color=cmap[(i+2)%colornumber],legend='legend_amplitude')
                s4.line(x='Cycle_number',y='I_response',source=responsesource,color=cmap[(i+2)%colornumber],legend='legend_amplitude')
                s4.circle(x='Cycle_number',y='Phase_response',source=responsesource,y_range_name="Phase_response",color=cmap[i],legend='legend_phase')
                s4.line(x='Cycle_number',y='Phase_response',source=responsesource,y_range_name="Phase_response",color=cmap[i],legend='legend_phase')

                i+=1

        # s1.add_tools(HoverTool(tooltips=[( 'Filenames',   '@filenames')],mode='mouse'))
        # s2.add_tools(HoverTool(tooltips=[( 'Filenames',   '@filenames')],mode='mouse'))

        if self.checkBox_4.isChecked():
            s4.extra_y_ranges={'Phase_response':Range1d(start=0,end=0.3)}
            s4.add_layout(LinearAxis(y_range_name="Phase_response",axis_label='Phase Response'), 'right')
            s4.y_range=Range1d(0.,1)


            s4.add_tools(HoverTool(tooltips=[( 'Filenames',   '@legend')],mode='mouse'))

            new_legend = s4.legend[0]
            s4.legend[0].plot = None
            s4.add_layout(new_legend, 'right')
            s4.legend.click_policy="hide"
            s4.xaxis.axis_label='Cycle number'
            s3.output_backend = "svg"
            s4.output_backend = "svg"

        if self.checkBox_3.isChecked():
            s3.add_tools(HoverTool(tooltips=[( 'Filenames',   '@legend')],mode='mouse'))
            new_legend = s3.legend[0]
            s3.legend[0].plot = None
            s3.add_layout(new_legend, 'right')
            s3.legend.click_policy="hide"
            s3.xaxis.axis_label='Time(s)'
            s3.yaxis.axis_label='Current Amplitude(A)'

        s1.legend.location = "top_right"
        s1.legend.orientation = "vertical"

        new_legend = s1.legend[0]
        s1.legend[0].plot = None
        s1.add_layout(new_legend, 'right')
        s1.legend.click_policy="hide"
        s1.yaxis.axis_label='Current(A)'
        s1.xaxis.axis_label='Time(s)'


        new_legend = s2.legend[0]
        s2.legend[0].plot = None
        s2.add_layout(new_legend, 'right')
        s2.legend.click_policy="hide"
        s2.legend.location = "top_right"
        s2.legend.orientation = "vertical"
        s2.xaxis.axis_label='Time(s)'
        s2.yaxis.axis_label='Phase'
        #w



        new_legend = s5.legend[0]
        s5.legend[0].plot = None
        s5.add_layout(new_legend, 'right')
        s5.legend.click_policy="hide"
        s5.legend.location = "top_right"
        s5.legend.orientation = "vertical"
        s5.xaxis.axis_label='Time(s)'
        s5.yaxis.axis_label='Temperature(C)'
        # s4.yaxis.axis_label='Response'


        s1.output_backend = "svg"
        s2.output_backend = "svg"
        s5.output_backend = "svg"
        # show(column(s3,s4))
        show(column(whatplot))
        return



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    setting = QtWidgets.QMainWindow()
    ui = Ui_setting()
    ui.setupUi(setting)
    setting.show()
    app.exec_()


ui=None
setting=None
app=None
print('Done')

###
