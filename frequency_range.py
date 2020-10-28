def FrequencyRange(startpoint,endpoint,samples,middlepoint=[]):
    frequencies = np.logspace(np.log10(startpoint), np.log10(endpoint), num=samples)\
    if len(middlepoint)==0:
        frequency_start =[startpoint]
        frequency_end =[endpoint]
        npoint =[samples]
        return frequency_start, frequency_end, npoint
    frequency_start = [startpoint]
    frequency_end = [endpoint]
    npoint = []
    for i in range(len(middlepoint)):
        mp=middlepoint[i]
        frequency_start.append()
    frequency_start = [startFrequency, frequencies[middlepoint + 1]]
    frequency_end = [frequencies[middlepoint], endFrequency]
    npoint = [middlepoint, len(frequencies) - middlepoint]
    return frequency_start,frequency_end,npoint