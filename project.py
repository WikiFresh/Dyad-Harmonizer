import time
import matplotlib
import sounddevice as sd
import scipy
import numpy as np
from scipy.io import wavfile as wav
from scipy.io.wavfile import write, read
from scipy import fftpack as scfft, fft
# from scipy.fft import fft, fftfreq
from matplotlib import pyplot as plt

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
write('output.wav', sps_hz, my_recording)

# 2. Apply FFT on recording to get highest audible frequency:
fs_rate, signal = read("output.wav")
l_audio = len(signal.shape)
N = signal.shape[0]
secs = N / float(fs_rate)
Ts = 1.0 / fs_rate
t = np.arange(0, secs, Ts)
FFT = abs(scipy.fft.fft(signal))
FFT_side = FFT[range(N // 2)]
freqs = scipy.fftpack.fftfreq(signal.size, t[1] - t[0])
fft_freqs = np.array(freqs)
freqs_side = freqs[range(N // 2)]
fft_freqs_side = np.array(freqs_side)
spectrum, freqs, line = plt.magnitude_spectrum(signal, fs_rate)
max_idx = np.argmax(spectrum)
HighestAudibleFrequency = freqs[max_idx]
print(HighestAudibleFrequency)

plt.show()

# 4. Generate a tone:
tone_duration_s = 5

# To find the fifth of a note, multiply its frequency by 1.5
fifth_freq_hz = int(HighestAudibleFrequency * 1.5)

each_sample_number = np.arange(tone_duration_s * sps_hz)
waveform = np.sin(2 * np.pi * each_sample_number * fifth_freq_hz / sps_hz)
# Tone down the amplitude by a factor of 0.3
waveform_quiet = waveform * 0.3
# Convert to 16 bits (2^16 = 65536, 65536/2 = 32768 (x-axis to peak))
waveform_integers = np.int16(waveform_quiet * 32768)
write('perfect_fifth_sine.wav', sps_hz, waveform_integers)
