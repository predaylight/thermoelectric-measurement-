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
path='C:\\Users\\vcostanz\\Desktop\\Linghui\\test_sweeper\\*.csv'
#path='C:\\Users\\vcostanz\\Desktop\\Linghui\\Humidity-Time-Superposition\\s1\\wet3\\*.txt'

i = 0
length = []
ni = 2
voltage=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
onset=[]
p=[]
abs=[]
phase=[]
tanloss=[]
imag=[]
onset=[]
for name in glob.glob(path):
    tname = name.split('\\')[-1]
    voltage=float(tname.split('V')[0])
    print(tname)
    print('the voltage is ',voltage)

    data=pd.read_csv(name,sep='\t')
    print(data.head())
    tloss=np.array(data['x'].values)/np.array(data['y'].values)
    freq=np.array(data['frequency'].values)
    setonarg=np.argmax(tloss[freq<1e5])
    cre=np.array(data['x'].values)/voltage

    onset.append([freq[setonarg], cre[setonarg]])
    p.append(go.Scatter(x=np.log10(freq/cre[setonarg]), y=np.log10(cre/cre[setonarg]),
                           mode='markers',
                           name=tname))
    abs.append(go.Scatter(x=data['frequency'].values, y=data['abs'].values,
                        mode='markers',
                        name=tname))
    phase.append(go.Scatter(x=data['frequency'].values, y=data['phs'].values,
                        mode='markers',
                        name=tname))
    tanloss.append(go.Scatter(x=data['frequency'].values, y=tloss,
                        mode='markers',
                        name=tname))
    imag.append(go.Scatter(x=data['frequency'].values, y=data['y'].values,
                        mode='markers',
                        name=tname))
       # data file; freq,amp,phase;
    i += 1
onset=np.transpose(onset)
p.append(go.Scatter(x=np.log10(onset[0,:]), y=np.log10(onset[1,:]),
                           mode='markers',
                       marker=dict(size=8,color='black'),
                           name='Onset'))
layout = go.Layout(
    autosize=False,
    width=800,
    height=600,
    xaxis=dict(
        title='log Frequency ',
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
        title='log real conductivity',
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
# Put graph object together and plot
figure = dict(data=p, layout=layout)
pyo.plot(figure, config=graph_configure)

layout2 = go.Layout(
    autosize=False,
    width=800,
    height=600,
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
        title='log abs',
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
figure = dict(data=abs, layout=layout2)
pyo.plot(figure, config=graph_configure)

layout = go.Layout(
    autosize=False,
    width=800,
    height=600,
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
        title='phase',
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
# Put graph object together and plot
figure = dict(data=phase, layout=layout)
pyo.plot(figure, config=graph_configure)
figure = dict(data=tanloss, layout=layout)
pyo.plot(figure, config=graph_configure)
figure = dict(data=imag, layout=layout)
pyo.plot(figure, config=graph_configure)