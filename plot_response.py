import numpy as np

import glob
import os
import math

import plotly
from plotly import graph_objs as go
from plotly import offline as pyo
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import scipy as sp
from scipy.signal import *



path='C:\\Users\\vcostanz\\Desktop\\Linghui\\P3_A\\sample6\\tsweep\\*.txt'
response_plot=[]
current_temp=[]
temp_plot=[]
files=[]
response_t=[]
avg_response=[]
std_response=[]
for name in glob.glob(path):
    sname=name.split('/')[-1]
    # sname=sname.split('_')[-1]
    # sname=sname.split('.')[0]
    files.append(sname)
order=np.argsort(files)
files=np.array(files)
ordered_files=np.array(glob.glob(path))[order]

for name in ordered_files:
    tname = name.split('\\')[-1]
    sname=name.split('/')[-1]
    sname=sname.split('_')[-1]
    tname=sname.split('.')[0]
    data=pd.read_csv(name,sep='\t')
    print(data.head())
    amp = np.array(data['abs'].values)
    phs = np.array(data['phs'].values)
    temperature = np.array(data['temperature'].values)
    time = np.cumsum(data['time'].values)

    I_highT=sp.signal.find_peaks(temperature,height=30,distance=1000)[0]
    I_lowT=sp.signal.find_peaks(-temperature,height=-20,distance=1000)[0]
    lowlength=min(len(I_highT),len(I_lowT))
    print(len(I_highT))
    I_lowT=I_lowT[:lowlength]
    I_highT=I_highT[:lowlength]

    print(len(I_lowT))
    response=amp[I_highT]/amp[I_lowT]
    avg_response.append(np.mean(response[1:]))
    std_response.append(np.std(response[1:]))

    current_temp = make_subplots(specs=[[{"secondary_y": True}]])

    current_temp.add_trace(go.Scatter(x=time[::50], y=amp[::50],
                           mode='lines',
                           name=tname+'_amp'),
                            secondary_y=False)
    current_temp.add_trace(go.Scatter(x=time[::50], y=temperature[::50],
                                   mode='lines',
                                   name=tname+'_temperature'),
                            secondary_y=True)
    # response_plot.append(go.Scatter(x=np.arange(len(response)), y=response,
    #                                mode='markers',
    #                                name='response'))
    # temp_plot.append(go.Scatter(x=np.arange(len(response)), y=temperature[I_highT],
    #                                mode='markers',
    #                                name='High T'))
    # temp_plot.append(go.Scatter(x=np.arange(len(response)), y=temperature[I_lowT],
    #                                mode='markers',
    #                                name='lowT'))



layout = go.Layout(
    autosize=True,
    # width=800,
    # height=600,
    xaxis=dict(
        title='time ',
        linewidth=1.5,
        ticks='outside',
        type='linear',
        showgrid=False,
        titlefont=dict(
            family='Helvetica',
            size=14
        ),
        automargin=True,
        autorange=True,
        mirror=True,
    ),
    yaxis=dict(
        title='log abs conductivity',
        linewidth=1.5,
        type='log',
        ticks='outside',
        showgrid=False,
        titlefont=dict(
            family='Helvetica',
            size=14
        ),
        automargin=True,
        autorange=True,
        mirror=True,
    ))
layout2 = go.Layout(
    autosize=True,
    # width=800,
    # height=600,
    xaxis=dict(
        title=' Temp ',
        linewidth=1.5,
        ticks='outside',
        type='linear',
        showgrid=False,
        titlefont=dict(
            family='Helvetica',
            size=14
        ),
        automargin=True,
        autorange=True,
        mirror=True,
    ),
    yaxis=dict(
        title=' ',
        linewidth=1.5,
        type='linear',
        ticks='outside',
        showgrid=False,
        titlefont=dict(
            family='Helvetica',
            size=14
        ),
        automargin=True,
        autorange=True,
        mirror=True,
    ))

graph_configure = dict(
    displayModeBar=True,
    showSendToCloud=False,
    toImageButtonOptions=dict(
        format='svg',
    ),
    displaylogo=False,
    watermark=False,
    responsive=True,
)

# response_t.append(go.Scatter(x=np.int_(files[order]),y=avg_response,
#                     error_y=dict(
#                         type='data',
#                         array=std_response,
#                         visible=True
#                     ),
#                     mode='markers+lines',
#                     name='response'))
# Put graph object together and plot
current_temp.show()

# figure2 = dict(data=response_plot, layout=layout2)
# pyo.plot(figure2, config=graph_configure)
#
# figure3 = dict(data=temp_plot, layout=layout2)
# pyo.plot(figure3, config=graph_configure)

# figure4 = dict(data=response_t, layout=layout2)
# pyo.plot(figure4, config=graph_configure)

# response_plot=[]
# current_temp=[]
# temp_plot=[]
# for name in glob.glob(path):
#     tname = name.split('\\')[-1]
#     data=pd.read_csv(name,sep='\t')
#     print(data.head())
#     amp = np.array(data['abs'].values)
#     phs = np.array(data['phs'].values)
#     temperature = np.array(data['temperature'].values)
#     time = np.cumsum(data['time'].values)
#
#     I_highT=sp.signal.find_peaks(temperature,height=40,distance=1000)[0]
#     I_lowT=sp.signal.find_peaks(-temperature,height=-20,distance=1000)[0]
#     lowlength=min(len(I_highT),len(I_lowT))
#     print(len(I_highT))
#     I_lowT=I_lowT[:lowlength]
#     I_highT=I_highT[:lowlength]
#
#     print(len(I_lowT))
#     response=amp[I_highT]/amp[I_lowT]
#     current_temp.append(go.Scatter(x=time[::50], y=amp[::50],
#                            mode='lines',
#                            name=tname))
#     response_plot.append(go.Scatter(x=np.arange(len(response)), y=response,
#                                    mode='markers',
#                                    name='response'))
#     temp_plot.append(go.Scatter(x=np.arange(len(response)), y=temperature[I_highT],
#                                    mode='markers',
#                                    name='High T'))
#     temp_plot.append(go.Scatter(x=np.arange(len(response)), y=temperature[I_lowT],
#                                    mode='markers',
#                                    name='lowT'))
#
#
#
# layout = go.Layout(
#     autosize=True,
#     # width=800,
#     # height=600,
#     xaxis=dict(
#         title='time ',
#         linewidth=1.5,
#         ticks='outside',
#         type='linear',
#         showgrid=False,
#         titlefont=dict(
#             family='Helvetica',
#             size=14
#         ),
#         automargin=True,
#         autorange=True,
#         mirror=True,
#     ),
#     yaxis=dict(
#         title='log abs conductivity',
#         linewidth=1.5,
#         type='log',
#         ticks='outside',
#         showgrid=False,
#         titlefont=dict(
#             family='Helvetica',
#             size=14
#         ),
#         automargin=True,
#         autorange=True,
#         mirror=True,
#     ))
# layout2 = go.Layout(
#     autosize=True,
#     # width=800,
#     # height=600,
#     xaxis=dict(
#         title=' Temp ',
#         linewidth=1.5,
#         ticks='outside',
#         type='linear',
#         showgrid=False,
#         titlefont=dict(
#             family='Helvetica',
#             size=14
#         ),
#         automargin=True,
#         autorange=True,
#         mirror=True,
#     ),
#     yaxis=dict(
#         title=' ',
#         linewidth=1.5,
#         type='linear',
#         ticks='outside',
#         showgrid=False,
#         titlefont=dict(
#             family='Helvetica',
#             size=14
#         ),
#         automargin=True,
#         autorange=True,
#         mirror=True,
#     ))
#
# graph_configure = dict(
#     displayModeBar=True,
#     showSendToCloud=False,
#     toImageButtonOptions=dict(
#         format='svg',
#     ),
#     displaylogo=False,
#     watermark=False,
#     responsive=True,
# )
# # Put graph object together and plot
# figure = dict(data=current_temp, layout=layout)
# pyo.plot(figure, config=graph_configure)
#
# figure2 = dict(data=response_plot, layout=layout2)
# pyo.plot(figure2, config=graph_configure)
#
# figure3 = dict(data=temp_plot, layout=layout2)
# pyo.plot(figure3, config=graph_configure)
#
#
#
