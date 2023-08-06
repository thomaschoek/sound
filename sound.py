import sounddevice as sd
import numpy as np
import time

# sd.query_devices() geeft een lijst van alle beschikbare geluidsoutputs / inputs op je computer. Je kiest er een, bijvoorbeeld 'default' en leest de samplerate uit d.w.z. het aantal 'traptreden' van een gedigitaliseerde/discrete benadering van een continu geluidssignaal, ofwel samples, dat hij per seconde kan verwerken

# op mijn pc werkt geluidsoutput 0, maar bij jou is het misschien 2 of 3 of 4 of 10, weet nog niet hoe ik dit kan standaardiseren...

samplerate = sd.default.samplerate = sd.query_devices(0)['default_samplerate']
sd.default.channels = 1 # zet op 2 voor stereogeluid
sd.default.device = 1

frequency = 220 # frequentie van de toon bijv. 440 voor een A
amplitude = 0.5 # amplitude van geluidsgolf
t = 1 # tijd van toon in seconden

sine_waves = np.sin(
        np.arange(samplerate * t, dtype=np.float32) * amplitude * 2 * np.pi * frequency / samplerate
)
sine_waves = sine_waves.reshape(-1, 1)

stream = sd.OutputStream()

stream.start()

stream.write(sine_waves)

stream.stop()

stream.close()

# dit is dus een heel simpel voorbeeld maar je kan natuurlijk ook dingen doen als

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
#    import ipdb; ipdb.set_trace()
    print(f"steps: {steps}")
    duration = iterations * steps * note_length
    end = time.time() + duration
    while time.time() < end:
        frequency = base_frequency
        for i in range(steps):
            data = get_sine_waves(samplerate, note_length, amplitude, frequency)
            output.write(data)
            frequency *= ratio % base_frequency * 2
#        amplitude *= 0.5

def fractal_arpeggio_up(output, note_length=0.5, base_frequency=44):
    arpeggio_up(output, note_length=note_length, base_frequency=base_frequency)
    fractal_arpeggio_up(output, note_length=note_length * 0.7, base_frequency=base_frequency * 1.5)

def pythagorean_fractal(output, note_length=0.0625, k=12):
    a = k # 12
    b = k - 1 # 11
    c = np.sqrt(a * a + b * b) # 144 + 121 = 265, sqrt(265) is not an integer
    c_squared = c * c
    # I want a and b to be both integers


    b = np.sqrt(b)
    arpeggio_up(output, note_length=note_length, steps=c)
    pythagorean_fractal(output, note_length=note_length, a=c, b=b)


stream = sd.OutputStream()

stream.start()

pythagorean_fractal(output=stream)

stream.close()
