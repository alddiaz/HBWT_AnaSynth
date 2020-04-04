# HBWT_AnaSynth example
# Developed by Aldo Diaz
# University of Campinas, 2015

import lib.libhbwt as HBWT_Ana # HBWT Analysis
import lib.libihbwt as HBWT_Synth # HBWT Synthesis
from scipy.signal import daub, qmf # Daubechies wavelets
from scipy.io import wavfile # WAV files
from lib.float32 import * # 'float32' input data normalization
from lib.estimatef0 import * # fundamental frequency estimation
import numpy as np # (AUX) numeric library
import matplotlib.pyplot as plt # (AUX) graphics library
import os as os # (AUX) operating system commands

# Load input signal
fs, x = wavfile.read('./input/qC-G4-1-tu.wav') # input signal 'x'
x, data_type = float32(x) # data normalization

# Model parameters
h       = daub(11) # Daubechies-11 low pass filter coefficients
g       = qmf(h) # Daubechies-11 high pass filter coefficients
f0, P   = estimatef0(x, fs) # f0: estimated fundamental frequency of input signal 'x' (Hertz)
                            # P: estimated (integer) signal period (given in number of samples)
N = 5 # levels of wavelet decomposition

# Analysis step
a, b, cmfb = HBWT_Ana.hbwt(x, h, g, P, N)

# Synthesis step
y = HBWT_Synth.ihbwt(a, b, h, g) # reconstructed signal 'y'
y = ifloat32(x, data_type) # Data back normalization
wavfile.write('./output/synth_sig.wav', fs, y) # write WAV output file

## Plots
plt.ion()
plt.close('all')

# Input signal x[n]
plt.figure(1)
plt.plot(np.arange(len(x))/float(fs), x, 'b')
plt.title('Signal x(t)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()

# DFT spectrum magnitude
NFFT    = 32*1024
X       = np.fft.fftshift(np.fft.fft(x, NFFT))
Xmag    = np.abs(X[NFFT/2:]) # DFT spectrum
fVals   = fs*np.arange(NFFT/2)/NFFT
fig_dft     = plt.figure(2)
ax          = fig_dft.add_subplot(111)
x_tick      = f0*np.arange(0, int(fVals[-1]/f0)) # x axis labels
x_label     = [ r"$0$" ]
x_label.extend([ r"$f"+str(i)+"$" for i in range(0, int(fVals[-1]/f0)) ])
plt.plot(fVals, Xmag, 'b')
ax.set_xticks(x_tick)
ax.set_xticklabels(x_label, fontsize=10)
plt.xlim([ 0, 6*f0 ]) # limited number of harmonics
ax.xaxis.grid(True)
plt.title('Signal x(t) - Magnitude spectrum, f0 = '+str(np.round(f0,1))+" Hz")
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.tight_layout()

# CMFB magnitude spectrum
CMFB    = np.fft.fftshift(np.fft.fft(cmfb[::-1,:], NFFT, axis=0))
CMFBmag = abs(CMFB[NFFT/2:]) # CMFB spectrum
omega   = 2*np.pi*np.arange(NFFT/2)/NFFT # Normalized frequency in rad
fig_cmfb    = plt.figure(3)
ax          = fig_cmfb.add_subplot(111)
x_tick      = np.pi*np.arange(0,P+1)/P # x axis labels
x_label     = [ r"$0$", r"$\pi/"+str(P)+"$" ]
x_label.extend([ r"$"+str(i)+"\pi/"+str(P)+"$" for i in range(2, P) ])
x_label.extend([ r"$\pi$" ])
ax.plot(omega, CMFBmag)
ax.set_xticks(x_tick)
ax.set_xticklabels(x_label, fontsize=10)
ax.axis([ 0, 8*np.pi/P, 0, 1.1*CMFBmag.max() ]) # limited spectrum
ax.xaxis.grid(True)
plt.title('Cosine-Modulated Filter Bank spectrum, P = '+str(P)+' channels')
plt.xlabel('Normalized frequency (rad)')
plt.ylabel('Magnitude')
plt.tight_layout()

# DWT spectrum of filters H(z) and G(z)
DWTlo       = np.fft.fftshift(np.fft.fft(h, NFFT)) # DWT low pass filter
DWThi       = np.fft.fftshift(np.fft.fft(g, NFFT)) # DWT high pass filter
DWTlomag    = abs(DWTlo[NFFT/2:]) # DWT magnitude low pass filter
DWThimag    = abs(DWThi[NFFT/2:])
omega       = 2*np.pi*np.arange(NFFT/2)/NFFT # Normalized frequency in rad
fig_dwt     = plt.figure(4)
ax          = fig_dwt.add_subplot(111)
x_tick      = np.pi*np.arange(0,3)/2 # x axis labels
x_label     = [ r"$0$", r"$\pi/2$", r"$\pi$" ]
plt.plot(omega, DWTlomag, 'b', omega, DWThimag, 'm')
ax.set_xticks(x_tick)
ax.set_xticklabels(x_label, fontsize=10)
ax.axis([ 0, np.pi, 0, 1.1*DWTlomag.max() ]) # limited spectrum
ax.xaxis.grid(True)
plt.title('Discrete Wavelet Transform spectrum')
plt.xlabel('Normalized frequency (rad)')
plt.ylabel('Magnitude')
plt.tight_layout()

# Play the reconstructed signal
os.system('play ./output/synth_sig.wav')
