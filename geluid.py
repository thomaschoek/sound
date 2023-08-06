import sounddevice as sd
import numpy as np
import time

def get_sine_waves(samplerate, length, amplitude, frequency, data_type=np.float32):
    data = np.sin(
            np.arange(length * samplerate, dtype=data_type) * amplitude * 2 * np.pi * frequency / samplerate
    )
    data = data.reshape(-1,1)
    return data

def arpeggio_up(
        output,
        steps=6,
        samplerate=sd.default.samplerate,
        note_length=0.25,
        base_frequency=100,
        amplitude=0.5,
        ratio=1.5,
        iterations=1
    ):
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

def recursive_arpeggio_up(output, note_length=0.5, base_frequency=44):
    arpeggio_up(output, note_length=note_length, base_frequency=base_frequency)
    recursive_arpeggio_up(output, note_length=note_length * 0.7, base_frequency=base_frequency * 1.5)


def timed_arpeggio(output, total_time=3, note_length=0.125,base_frequency=100):
    steps = int(total_time / note_length)

    arpeggio_up(output=output, steps = steps, note_length=note_length, base_frequency=base_frequency)

def fibonacci_timed_arpeggio(output, iterations=7, base_frequency=100, fmod=1):
    prev = 0
    current = 1
    total_time = current
    frequency=base_frequency
    for i in range(iterations):
        timed_arpeggio(output,total_time=total_time, base_frequency=frequency)
        total_time += prev
        prev = current
        current = total_time
        frequency*=fmod

def harmonics(output, iterations=7):
    stream1 = sd.OutputStream()
    stream1.start()
    fibonacci_timed_arpeggio(output, iterations,base_frequency=100,fmod=1.1)
    fibonacci_timed_arpeggio(stream1, iterations, base_frequency=150,fmod=1.1)
    stream1.stop()
    stream1.close()


if __name__ == '__main__':

    samplerate = sd.default.samplerate = sd.query_devices(1)['default_samplerate'] # kies default geluidsoutput, meestal index 0
    sd.default.channels = 1 # monogeluid
    sd.default.device = 1
    
    stream = sd.OutputStream()
    stream.start()
    fibonacci_timed_arpeggio(stream,iterations=5)
    harmonics(stream,iterations=9)
    stream.stop()
    stream.close()
