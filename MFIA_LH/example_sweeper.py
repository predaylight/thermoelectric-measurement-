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

sweeper = daq.sweep()
sweeper.set('sweep/device', device)
sweeper.set('sweep/gridnode', 'oscs/%d/freq' % osc_index)
sweeper.set('sweep/start', 1e3)
sweeper.set('sweep/stop', 1e6)
samplecount = 100
sweeper.set('sweep/samplecount', samplecount)
sweeper.set('sweep/xmapping', 1)
sweeper.set('sweep/bandwidthcontrol', 2)
sweeper.set('sweep/bandwidthoverlap', 1)
sweeper.set('sweep/scan', 0)
sweeper.set('sweep/settling/time', 0)
sweeper.set('sweep/settling/inaccuracy', 0.001)
sweeper.set('sweep/averaging/tc', 16)
sweeper.set('sweep/averaging/sample', 20)
path = '/%s/demods/%d/sample' % (device, demod_index)
sweeper.subscribe(path)

sweeper.execute()

start = time.time()
timeout = 60  # [s]
while not sweeper.finished():  # Wait until the sweep is complete, with timeout.
        time.sleep(0.2)
        progress = sweeper.progress()
        print("Individual sweep progress: {:.2%}.".format(progress[0]), end="\r")
        # Here we could read intermediate data via:
        # data = sweeper.read(True)...
        # and process it while the sweep is completing.
        # if device in data:
        # ...
        if (time.time() - start) > timeout:
            # If for some reason the sweep is blocking, force the end of the
            # measurement.
            print("\nSweep still not finished, forcing finish...")
            sweeper.finish()

print("")
return_flat_dict = True
data = sweeper.read(return_flat_dict)
sweeper.unsubscribe(path)
sweeper.clear()

# Check the dictionary returned is non-empty.
assert data, "read() returned an empty data dictionary, did you subscribe to any paths?"
# Note: data could be empty if no data arrived, e.g., if the demods were
# disabled or had rate 0.
assert path in data, "No sweep data in data dictionary: it has no key '%s'" % path
samples = data[path]
print("Returned sweeper data contains", len(samples), "sweeps.")