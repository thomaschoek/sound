import sounddevice as sd
import numpy as np
import time
import threading as thrd
from geluid import *

def polyphonic_arps(sd=sd, iterations=7):
    stream_a = sd.OutputStream()
    stream_b = sd.OutputStream()
    stream_a.start()
    stream_b.start()
    a = thrd.Thread(target=fibonacci_timed_arpeggio, kwargs={'sd':sd, 'iterations':iterations,'base_frequency':100,'fmod':1})
    b = thrd.Thread(target=fibonacci_timed_arpeggio, kwargs={'sd':sd, 'iterations':iterations,'base_frequency':300, 'fmod' : 1})
    b.start()
    a.start()
    while a.is_alive() or b.is_alive():
        pass
    stream_a.stop()
    stream_b.stop()
    stream_a.close()
    stream_b.close()


if __name__ == '__main__':

    import sys
    sd_index = int(sys.argv[1])

    iterations = int(sys.argv[2])

    samplerate = sd.default.samplerate = sd.query_devices(sd_index)['default_samplerate'] # kies default geluidsoutput, meestal index 0
    sd.default.channels = 1 # monogeluid
    sd.default.device = sd_index

    # fibonacci_timed_arpeggio(stream,iterations=5)
    polyphonic_arps(iterations=iterations)
