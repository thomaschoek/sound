import sounddevice as sd
import numpy as np
import time
import threading as thrd
from geluid import *

samplerate = sd.default.samplerate = sd.query_devices(1)['default_samplerate'] # kies default geluidsoutput, meestal index 0
sd.default.channels = 1 # monogeluid
sd.default.device = 1


def polyphonic_arps():
    x = thrd.Thread(target=


if __name__ == '__main__':
    stream = sd.OutputStream()
    stream.start()
    fibonacci_timed_arpeggio(stream,iterations=5)
    harmonics(stream,iterations=9)
    stream.stop()
    stream.close()
