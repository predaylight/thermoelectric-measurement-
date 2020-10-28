import numpy as np

print(np.__version__)
import glob
import os
import math

import plotly
from plotly import graph_objs as go
from plotly import offline as pyo
import pandas as pd

filenames = []
data = []
real=[]
nyquist = []
scaled=[]
# bode=[]
# voltage=[]
path='C:\\Users\\vcostanz\\Desktop\\Linghui\\P6\\P6ABA,CoCl2,1v2\\Taped\\*.csv'

#path='C:\\Users\\vcostanz\\Desktop\\Linghui\\Humidity-Time-Superposition\\s1\\wet3\\*.txt'

i = 0
length = []
ni = 2
onset=[]
p=[]
abs=[]
phase=[]
tanloss=[]
imag=[]
onset=[]
voltage=[0.01]*len(glob.glob(path))

order=[]
for name in glob.glob(path):
    temp=name.split('\\')[-1]
    temp=temp.split('_')[-2]
    order.append(int(temp.split('temp')[0]))
print(order)
order_index=np.argsort(order)
ordered_files=np.array(glob.glob(path))
ordered_files=ordered_files[order_index]
for name in ordered_files:
    tname = name.split('\\')[-1]
    voltage=float(tname.split('V')[0])
    print(tname)
    print('the voltage is ',voltage)

    data=pd.read_csv(name,sep='\t')
    print(data.head())
    amp = np.array(data['abs'].values)
    phs = np.array(data['phs'].values)
    freq = np.array(data['frequency'].values)
    cre = amp * np.cos(phs) / voltage
    cim = amp * np.sin(phs) / voltage
    tloss = cre / cim
    epsilon_im=cre/(freq*2*math.pi)
    p.append(go.Scatter(x=freq, y=cre,
                           mode='markers',
                           name=tname))
    # abs.append(go.Scatter(x=data['frequency'].values, y=data['abs'].values,
    #                     mode='markers',
    #                     name=tname))
    # phase.append(go.Scatter(x=data['frequency'].values, y=data['phs'].values,
    #                     mode='markers',
    #                     name=tname))
    tanloss.append(go.Scatter(x=data['frequency'].values, y=tloss,
                        mode='markers',
                        name=tname))
    # imag.append(go.Scatter(x=data['frequency'].values, y=data['y'].values,
    #                     mode='markers',
    #                     name=tname))
    #    # data file; freq,amp,phase;
    i += 1

layout = go.Layout(
    autosize=True,
    # width=800,
    # height=600,
    xaxis=dict(
        title='log Frequency ',
        linewidth=1.5,
        ticks='outside',
        type='log',
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
        title='log real conductivity',
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
# Put graph object together and plot
figure = dict(data=p, layout=layout)
pyo.plot(figure, config=graph_configure)
#
# layout2 = go.Layout(
#     autosize=False,
#     width=800,
#     height=600,
#     xaxis=dict(
#         title='log Frequency ',
#         linewidth=1.5,
#         ticks='outside',
#         type='log',
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
#         title='log abs',
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
# figure = dict(data=abs, layout=layout2)
# pyo.plot(figure, config=graph_configure)
#
# layout = go.Layout(
#     autosize=False,
#     width=800,
#     height=600,
#     xaxis=dict(
#         title='log Frequency ',
#         linewidth=1.5,
#         ticks='outside',
#         type='log',
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
#         title='phase',
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
# figure = dict(data=phase, layout=layout)
# pyo.plot(figure, config=graph_configure)
figure = dict(data=tanloss, layout=layout)
pyo.plot(figure, config=graph_configure)
# figure = dict(data=imag, layout=layout)
# pyo.plot(figure, config=graph_configure)