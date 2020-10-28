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
startFrequency = 100
endFrequency = 100e3
samples = 20

lockIn.setAmplitude(0.1)
lockIn.setFrequency(endFrequency)
lockIn.autoRange()
print('autorange')

lockIn.sweeperSet(startFrequency, endFrequency, samples)
lockIn.sweeperStart()
status = lockIn.sweeperStatus()
print(status)
while not status['done']:
    time.sleep(1)
    data = lockIn.sweeperRead()
    # if not data['nan']: print(data)
    if bool(data): print(data['nan'])
    status = lockIn.sweeperStatus()


print(data)
lockIn.sweeperClose()

lockIn.adjustRange(10e-9)
instant = lockIn.pollData()
