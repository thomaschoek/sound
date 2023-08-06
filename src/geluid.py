import numpy as np
import time

def get_sine_waves(samplerate, length, amplitude, frequency, data_type=np.float32):
    data = np.sin(
            np.arange(length * samplerate, dtype=data_type) * amplitude * 2 * np.pi * frequency / samplerate
    )
    data = data.reshape(-1,1)
    return data

def arpeggio_up(
        sd, #sounddevice
        steps=6,
        note_length=0.25,
        base_frequency=100,
        amplitude=0.5,
        ratio=1.5,
        iterations=1
    ):
    samplerate = sd.default.samplerate
    output = sd.OutputStream()
    output.start()
    duration = iterations * steps * note_length
    end = time.time() + duration
    while time.time() < end:
        frequency = base_frequency
        for i in range(steps):
            data = get_sine_waves(samplerate, note_length, amplitude, frequency)
            output.write(data)
            frequency *= ratio
            frequency %= (base_frequency * 4)
            frequency += base_frequency
    output.stop()
    output.close()

def recursive_arpeggio_up(sd, note_length=0.5, base_frequency=44):
    arpeggio_up(sd, note_length=note_length, base_frequency=base_frequency)
    recursive_arpeggio_up(sd, note_length=note_length * 0.7, base_frequency=base_frequency * 1.5)


def timed_arpeggio(sd, total_time=3, note_length=0.125,base_frequency=100):
    steps = int(total_time / note_length)

    arpeggio_up(sd=sd, steps = steps, note_length=note_length, base_frequency=base_frequency)

def fibonacci_timed_arpeggio(sd, iterations=7, base_frequency=100, fmod=1):
    prev = 0
    current = 1
    total_time = current
    frequency=base_frequency
    for i in range(iterations):
        timed_arpeggio(sd,total_time=total_time, base_frequency=frequency)
        total_time += prev
        prev = current
        current = total_time
        frequency*=fmod

def harmonics(sd, iterations=7):
    
    fibonacci_timed_arpeggio(sd, iterations,base_frequency=100,fmod=1.1)
    fibonacci_timed_arpeggio(sd, iterations, base_frequency=150,fmod=1.1)


if __name__ == '__main__':

    samplerate = sd.default.samplerate = sd.query_devices(1)['default_samplerate'] # kies default geluidsoutput, meestal index 0
    sd.default.channels = 1 # monogeluid
    sd.default.device = 1
    
    fibonacci_timed_arpeggio(sd,iterations=5)
    harmonics(sd,iterations=9)
