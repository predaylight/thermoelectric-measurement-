import zhinst
import zhinst.utils
import zhinst.ziPython
import time
import numpy as np
import math

deviceID = 'dev3275'
apiLevel = 6
err_msg = "Impossible to create the API session."

(daq, device, props) = zhinst.utils.create_api_session(deviceID, apiLevel,
                                                   required_devtype='.*LI|.*IA|.*IS',
                                                   required_err_msg=err_msg)

out_channel = 0
out_mixer_channel = zhinst.utils.default_output_mixer_channel(props)
in_channel = 0
demod_index = 0
osc_index = 0
demod_rate = 100e3
time_constant = 1
frequency = 100e3
amplitude = 0.3
exp_setting = [['/%s/sigins/%d/ac'             % (device, in_channel), 0],
               ['/%s/sigins/%d/range'          % (device, in_channel), 2*amplitude],
               ['/%s/demods/%d/enable'         % (device, demod_index), 1],
               ['/%s/demods/%d/rate'           % (device, demod_index), demod_rate],
               ['/%s/demods/%d/adcselect'      % (device, demod_index), in_channel],
               ['/%s/demods/%d/order'          % (device, demod_index), 4],
               ['/%s/demods/%d/timeconstant'   % (device, demod_index), time_constant],
               ['/%s/demods/%d/oscselect'      % (device, demod_index), osc_index],
               ['/%s/demods/%d/harmonic'       % (device, demod_index), 1],
               ['/%s/oscs/%d/freq'             % (device, osc_index), frequency],
               ['/%s/sigouts/%d/on'            % (device, out_channel), 1],
               ['/%s/sigouts/%d/enables/%d'    % (device, out_channel, out_mixer_channel), 1],
               ['/%s/sigouts/%d/range'         % (device, out_channel), 1],
               ['/%s/sigouts/%d/amplitudes/%d' % (device, out_channel, out_mixer_channel), amplitude]]
daq.set(exp_setting)

# Unsubscribe any streaming data.
daq.unsubscribe('*')
time.sleep(10*time_constant)
daq.sync()

# Subscribe to the demodulator's sample node path.
path = '/%s/demods/%d/sample' % (device, demod_index)
poll_length = 0.001  # [s]
poll_timeout = 50  # [ms]
poll_flags = 0
poll_return_flat_dict = True

print("start measurement")
sampleAbs = []
samplePhs = []
start = []
endSubscribe = []
endPoll = []
endUnsubscribe = []
endFlush = []
end = []
daq.subscribe(path)

for i in range(0,10):
    start.append(time.time())
    # daq.subscribe(path)
    # endSubscribe.append(time.time())
    # daq.unsubscribe('*')
    # endUnsubscribe.append(time.time())
    daq.flush()
    endFlush.append(time.time())
    data = daq.poll(poll_length, poll_timeout, poll_flags, poll_return_flat_dict)
    endPoll.append(time.time())
    sample = data[path]
    sampleAbs.append(np.mean(np.abs(sample['x'] + 1j * sample['y'])))
    samplePhs.append(np.mean(np.angle(sample['x'] + 1j * sample['y'])))
    end.append(time.time())

daq.unsubscribe('*')

print("Mean Value current: {}".format(np.mean(sampleAbs)))
print("poll time: {}".format(np.mean(endPoll) - np.mean(endFlush)))
print("Flush time: {}".format(np.mean(endFlush) - np.mean(start)))
# print("Subscribe time: {}". format(np.mean(endSubscribe) - np.mean(start)))
# print("poll time: {}".format(np.mean(endPoll) - np.mean(endSubscribe)))
# print("Unsubsrcibe Time: {}".format(np.mean(endUnsubscribe) - np.mean(endPoll)))
# print("Flush time: {}".format(np.mean(endFlush) - np.mean(endUnsubscribe)))
# print("append time: {}".format(np.mean(end) - np.mean(endFlush)))
print("total time: {}".format(np.mean(end) - np.mean(start)))

# sample = data[path]
# sample['R'] = np.abs(sample['x'] + 1j * sample['y'])
# sample['phi'] = np.angle(sample['x'] + 1j * sample['y'])
# print("Mean Value current: {}".format(np.mean(sample[i])))
# print("Impedance Abs: {}".format(amplitude/(np.mean(sample['R'])*math.sqrt(2))))
# print("Subscribe time: {}". format(endSubscribe - start))
# print("poll time: {}".format(endPoll - endSubscribe))
# print("Unsubsrcibe Time: {}".format(endUnsubscribe - endPoll))
# print("total time: {}".format(endUnsubscribe - start))

# daq.flush()
# imp_index = 0
# path = '/%s/imps/%d/sample' % (device, imp_index)
#
# start = time.time()
# daq.subscribe(path)
# endSubscribe = time.time()
# data = daq.poll(poll_length, poll_timeout, poll_flags, poll_return_flat_dict)
# endPoll = time.time()
# daq.unsubscribe('*')
# endUnsubscribe = time.time()
#
# impedanceSample = data[path]
# print("Average measured resitance: {} Ohm.".format(np.mean(impedanceSample['param0'])))
# print("Subscribe time: {}". format(endSubscribe - start))
# print("poll time: {}".format(endPoll - endSubscribe))
# print("Unsubsrcibe Time: {}".format(endUnsubscribe - endPoll))
# print("total time: {}".format(endUnsubscribe - start))
#
# daq.setInt('/%s/demods/0/enable' % device, 1)
# daq.sync()
# start = time.time()
# sample = daq.getSample('/%s/demods/0/sample' % device)
# end = time.time()
#
# sample['R'] = np.abs(sample['x'] + 1j*sample['y'])
# sample['phi'] = np.angle(sample['x'] + 1j*sample['y'])
#
#
# print("Mean Value current: {}".format(sample['R']))
# print("total time: {}".format(end - start))