import sys
sys.path.insert(0, 'C:\\Users\\vcostanz\\Desktop\\Linghui\\PYTHON\\MFIA_LH')
# sys.path.append('C:\\Users\\vcostanz\\Desktop\\Linghui\\PYTHON\\TemperatureBoard_LH')

sys.path.append('C:\\Users\\vcostanz\\Desktop\\Pyhton Projects\\TemperatureBoard')
from MFIA_LH import MFIA
from TemperatureBoard import TemperatureBoard
from multicycles_LH import tempsweep
# import PyQt5
import datetime
import time
import pandas as pd
import numpy as np
import os
import pandas as pd

def currentRange(data):
    dataf=pd.DataFrame(data=data)
    dataf.sort_values('frequency')
    abs=np.dataf['abs'].values
    minimum=abs[0]
    maximum=abs[-1]

