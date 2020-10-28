# -*- coding: utf-8 -*-
"""
Zurich Instruments LabOne Python API Example

Demonstrate how to perform a manually triggered autoranging for impedance while working in
manual range mode.
"""

# Copyright 2017 Zurich Instruments AG

from __future__ import print_function
import time
import zhinst.utils
import numpy as np


def autorange_current(deviceID,lockIn):
    oridata = lockIn.pollData()
    while len(oridata) == 0:
        oridata = lockIn.pollData()
    print(oridata)
    range_exp = np.round(np.log10(oridata['abs'])) + 2
    if range_exp<-6:
        range_exp=-6
        ###  so that the smallest range would be 1e-6. because it seems that when the range is lower than that the reading is inaccurate
    currentRange = lockIn.getCurrentRange(deviceID)
    t_start=time.time()
    timeout=20
    if currentRange != range_exp:
        while True:
            lockIn.adjustRange(10 ** (range_exp))
            time.sleep(1)
            data_range = lockIn.pollData()
            print('range adjustment:', 10 ** (range_exp))
            newrange_exp = np.round(np.log10(data_range['abs'])) + 2
            if newrange_exp <-6:
                break
            # if newrange_exp>-3:
            #     newrange_exp=-3
            # if newrange_exp<-6:
            #     newrange_exp=-6
            if newrange_exp == range_exp:
                currentRange = range_exp
                break
            range_exp = newrange_exp
            if time.time() - t_start > timeout:
                raise Exception("Autoranging failed after {} seconds.".format(timeout))

    # print('Voltage range changed from {:0.1e} V to {:0.1e} V.'.format(man_volt_range, auto_volt_range))

    return True
