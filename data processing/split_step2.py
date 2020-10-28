import numpy as np
import pandas as pd
import scipy
from skimage.restoration import denoise_tv_chambolle
# import statsmodels.tsa
# from statsmodels.tsa.stattools import kpss
# from statsmodels.tsa.stattools import adfuller
import math
#     from skimage.filters import denoise_tv_chambolle
# from split_step2 import split_step2

def split_step2(temperature,abs,phase,time,length,normtemp,difft):
    # denot=denoise_tv_chambolle(temperature,weight=0.3)
    denot=denoise_tv_chambolle(temperature,weight=0.2)
    diff=np.diff(denot)
    diff=np.insert(diff,0,0)
    x=np.arange(len(denot))
    # avg=np.mean(np.abs(diff))
    # dev=np.std(np.abs(diff))
    index2=x[np.abs(diff)>difft] # 0.032 for every 10 points

    # index2=scipy.signal.argrelextrema(diff,lambda x,y:np.abs(x-y)>avg,order=10)[0]

    plataus0=np.split(temperature,index2)
    time0=np.split(time,index2)
    absolute0=np.split(abs,index2)
    phase0=np.split(phase,index2)
    plataus=[]
    time1=[]
    absolute=[]
    phase1=[]

    avg_abs=[]
    avg_phase=[]
    avg_temp=[]
    std_abs=[]
    std_phase=[]
    std_temp=[]
    kpss_abs=[]

    for j in range(len(plataus0)):
        plotindex=plataus0[j]
        if len(plotindex)>length:
            plataus.append(plotindex)
            time1.append(time0[j])
            absolute.append(absolute0[j])
            phase1.append(phase0[j])
            avg_abs.append(np.mean(absolute0[j]))
            avg_phase.append(np.mean(phase0[j]))
            avg_temp.append(np.mean(plotindex))
            std_abs.append(np.std(absolute0[j]))
            std_phase.append(np.std(phase0[j]))
            std_temp.append(np.std(plotindex))

            ll=math.ceil(len(absolute0[j])/2)
            # tf=adfuller(absolute0[j][ll:],maxlag=55,autolag='t-stat')[1]<0.05
            # kpss_abs.append(tf)

    avg_abs=np.array(avg_abs)
    avg_phase=np.array(avg_phase)
    avg_temp=np.array(avg_temp)

    curvature_temp=np.diff(avg_temp)
    step=np.average(np.abs(curvature_temp))
    curvature_temp=np.insert(curvature_temp,0,0)
    curvature_temp=np.diff(curvature_temp)
    curvature_temp=np.append(curvature_temp,0)
    # step=np.average(np.abs(curvature_temp))
    steptf=curvature_temp>step*1

    cyclestart=np.array(range(len(avg_temp)))
    cyclestart=cyclestart[steptf]
    cyclelength=np.diff(cyclestart)
    iscyclestart=cyclelength>20
    iscyclestart=np.insert(iscyclestart,0,True)
    cyclestart=cyclestart[iscyclestart]


    split_abs=np.split(avg_abs,cyclestart)
    split_temp=np.split(avg_temp,cyclestart)
    split_phase=np.split(avg_phase,cyclestart)

    cyclen=len(split_abs)
    I_response=np.zeros(cyclen)
    Phase_response=np.zeros(cyclen)
    maxT=np.zeros(cyclen)
    minT=np.zeros(cyclen)
    maxI=np.zeros(cyclen)
    minI=np.zeros(cyclen)
    minPhase=np.zeros(cyclen)
    maxPhase=np.zeros(cyclen)
    for i in range(cyclen):
        if len(split_temp[i])>1:
            maxarg=np.argmax(split_temp[i])
            minarg=np.argmin(split_temp[i])
            maxT[i]=split_temp[i][maxarg]
            minT[i]=split_temp[i][minarg]
            maxI[i]=split_abs[i][maxarg]
            minI[i]=split_abs[i][minarg]
            minPhase[i]=split_phase[i][maxarg]
            maxPhase[i]=split_phase[i][minarg]
            I_response[i]=(maxI[i]-minI[i])/(minI[i]*(maxT[i]-minT[i]))
            Phase_response[i]=(maxPhase[i]-minPhase[i])/(maxT[i]-minT[i])


    # cyclestart=np.insert(cyclestart,0,0)
    cyclestart=np.insert(cyclestart,cyclen-1,len(avg_temp)-1)
    cyclenumber=range(len(cyclestart))
    cyclestart_temp=avg_temp[cyclestart]
    cyclestart_I=avg_abs[cyclestart]
    cyclestart_time=[time1[i][0] for i in cyclestart]

    nofeachcycle=np.diff(cyclestart)
    nofeachcycle[0]+=1
    cycleindex=np.array(range(len(nofeachcycle)))
    cycleindex=np.repeat(cycleindex,nofeachcycle)

    response=pd.DataFrame({'T_max':maxT,'T_minx':maxT,'I_max':maxI,'I_minx':maxI,'Phase_max':maxPhase,'Phase_minx':maxPhase,
                                'I_response':I_response,'Phase_response':Phase_response,
                                'Cycle_number':cyclenumber,'Cycle_start':cyclestart,
                                'time_cyclestart':cyclestart_time,'I_cyclestart':cyclestart_I,'T_cyclestart':cyclestart_temp})

    normindex=np.argmin(np.abs(np.array(avg_temp)-normtemp))
    normal_avg_abs=avg_abs/avg_abs[normindex]
    normal_std_abs=std_abs/avg_abs[normindex]
    newdict=pd.DataFrame(data={'time_sum':time1,'temperature':plataus,'abs':absolute,'phase':phase1
                                ,'T_mean':avg_temp,'I_mean':avg_abs,'Phase_mean':avg_phase,
                                'T_std':std_temp,'I_std':std_abs,'Phase_std':std_phase,#'I_kpss':kpss_abs,
                                'I_mean_normalized':normal_avg_abs,'I_std_normalized':normal_std_abs,
                                'Cycle_index':cycleindex
                                })
    print(response.head())
    print(newdict.head())
    return newdict,response,index2
