from MFIA import MFIA
import time

deviceID = 'dev3275'
amplitude = 0.3
frequency = 10e3
currentRange = 1e-6
demodRate = 100e3
samplingRate = 0.001


lockIn = MFIA(deviceID)

lockIn.set2TerminalMode(amplitude, frequency, currentRange, demodRate, samplingRate)
lockIn.begin()

time.sleep(2)

lockIn.setFrequency(10e+5)
lockIn.setAmplitude(0.1)
lockIn.autoRange()
print('autorange')
data = lockIn.pollData()

# lockIn.adjustRange(10e-9)
# data = []
# for i in range(0,10):
#     data = lockIn.pollData()
#     print(data["time"])
#     print(data["abs"])
# lockIn.end()
