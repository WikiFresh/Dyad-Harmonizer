import time
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write, read
from matplotlib import pyplot as plt
import simpleaudio as sa

# 1. Record sound from computer microphone:

rec_duration_s = 3
# Samples per second and recording duration
sps_hz = 44100
# Terminal prompt
print('Please begin recording:')
wait = 3
while wait > 0:
    print(wait)
    time.sleep(1)
    wait = wait - 1
if wait <= 0:
    print('START')
my_recording = sd.rec(int(rec_duration_s * sps_hz), samplerate=sps_hz, channels=1)
sd.wait()
write('input.wav', sps_hz, my_recording)

# 2. Apply FFT on recording to get highest audible frequency:
fs_rate, signal = read("input.wav")
spectrum, freqs, line = plt.magnitude_spectrum(signal, fs_rate)
max_idx = np.argmax(spectrum)
HighestAudibleFrequency = freqs[max_idx]
print(HighestAudibleFrequency)

# 4. Generate a tone:
tone_duration_s = 3

# To find the fifth of a note, multiply its frequency by 1.5
fifth_freq_hz = int(HighestAudibleFrequency * 1.5)

each_sample_number = np.arange(tone_duration_s * sps_hz)
waveform = np.sin(2 * np.pi * each_sample_number * fifth_freq_hz / sps_hz)
# Tone down the amplitude by a factor of 0.3
waveform_quiet = waveform * 0.3
# Convert to 16 bits (2^16 = 65536, 65536/2 = 32768 (x-axis to peak))
waveform_integers = np.int16(waveform_quiet * 32768)
write('perfect_fifth_sine.wav', sps_hz, waveform_integers)

wave_obj = sa.WaveObject.from_wave_file('perfect_fifth_sine.wav')
play_obj = wave_obj.play()
play_obj.wait_done()  # Wait until sound has finished playing

plt.show()
