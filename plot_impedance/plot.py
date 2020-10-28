import numpy as np

print(np.__version__)
import glob
import os
import math

import plotly
from plotly import graph_objs as go
from plotly import offline as pyo

filenames = []
data = []
real=[]
nyquist = []
scaled=[]
# bode=[]
# voltage=[]
path='C:\\Users\\vcostanz\\Desktop\\Linghui\\CaCl2_pectin_1112019\\film1\\*.txt'
#path='C:\\Users\\vcostanz\\Desktop\\Linghui\\Humidity-Time-Superposition\\s1\\wet3\\*.txt'

i = 0
length = []
ni = 2
voltage=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
onset=[]
bodeabs=[]
for name in glob.glob(path):
    tname = name.split('\\')[-1]

    #     voltage.append(float(tname.split(',')[0]))
    filenames = np.append(filenames, tname)
    print(filenames)
    f = np.transpose(np.genfromtxt(name, delimiter=';', skip_header=3 + ni * 2))
    print(np.shape(f))
    print(len(f[0]))
    freq = np.array(f[0])
    iim =np.array(f[2])
    ire = np.array(f[1])
    isquare=ire**2+iim**2

    zre = voltage[i]*ire/isquare
    zim = voltage[i]*iim/isquare

    cre = ire/voltage[i]
    cim = iim/voltage[i]

    onset0=int(np.argmax(cim))
    print(onset0)
    onset.append([freq[onset0], cre[onset0]])
    #     endre=len(zre)
    #     endim=len(zim)
    #     end=min(endre,endim)
    #     zre=zre[:end]
    #     zim=zim[:end]

    data.append(go.Scatter(x=freq, y=cre,
                           mode='markers',
                           name=tname))
    nyquist.append(go.Scatter(x=freq, y=cre/cim,
                              mode='markers',
                              name=tname))
    scaled.append(go.Scatter(x=freq, y=cim,
                              mode='markers',
                              name=tname))
    bodeabs.append(go.Scatter(x=freq, y=20*np.log10(isquare),
                             mode='markers',
                             name=tname))

    #     temp2=[]

    #     temp2.append(freq)
    #     temp2.append(zre)
    #     temp2.append(zim)
    #     nyquist.append(temp2)
    # data file; freq,amp,phase;
    i += 1
onset=np.transpose(onset)
data.append(go.Scatter(x=onset[0,:], y=onset[1,:],
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
figure = dict(data=data, layout=layout)
pyo.plot(figure, config=graph_configure)

# now data is a list, data[i] is the data corresponding to filenames[i]. The frequency is data[i][0], the y axis is data[i][1]
layout_nyquist = go.Layout(
    autosize=False,
    width=800,
    height=600,
    xaxis=dict(
        title='Real conductivity',
        linewidth=1.5,
        ticks='outside',
        showgrid=False,
        type='log',
        titlefont=dict(
            family='Helvetica',
            size=14
        ),
        automargin=True,
        autorange=True,
        mirror=True,
    ),
    yaxis=dict(
        title='-Imaginary Conductivity',
        linewidth=1.5,
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

graph_configure_nyquist = dict(
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
figure2 = dict(data=nyquist, layout=layout_nyquist)
pyo.plot(figure2, config=graph_configure_nyquist)

layout_scaled = go.Layout(
    autosize=False,
    width=800,
    height=600,
    xaxis=dict(
        title='freq',
        linewidth=1.5,
        ticks='outside',
        showgrid=False,
        type='log',
        titlefont=dict(
            family='Helvetica',
            size=14
        ),
        automargin=True,
        autorange=True,
        mirror=True,
    ),
    yaxis=dict(
        title='Scaled real Conductivity',
        linewidth=1.5,
        ticks='outside',
        showgrid=False,
        type='log',
        titlefont=dict(
            family='Helvetica',
            size=14
        ),
        automargin=True,
        autorange=True,
        mirror=True,
    ))

figure3 = dict(data=scaled, layout=layout_scaled)
pyo.plot(figure3, config=graph_configure_nyquist)

layout_scaled = go.Layout(
    autosize=False,
    width=800,
    height=600,
    xaxis=dict(
        title='freq',
        linewidth=1.5,
        ticks='outside',
        showgrid=False,
        type='log',
        titlefont=dict(
            family='Helvetica',
            size=14
        ),
        automargin=True,
        autorange=True,
        mirror=True,
    ),
    yaxis=dict(
        title='Scaled real Conductivity',
        linewidth=1.5,
        ticks='outside',
        showgrid=False,
        type='linear',
        titlefont=dict(
            family='Helvetica',
            size=14
        ),
        automargin=True,
        autorange=True,
        mirror=True,
    ))

figure4 = dict(data=bodeabs, layout=layout_scaled)
pyo.plot(figure4, config=graph_configure_nyquist)