# HBWT_AnaSynth example
# Developed by Aldo Diaz
# University of Campinas, 2015

import lib.libhbwt as HBWT_Ana # HBWT Analysis
import lib.libihbwt as HBWT_Synth # HBWT Synthesis
from scipy.signal import daub, qmf # Daubechies wavelets
from scipy.io import wavfile # WAV files
import numpy as np # (AUX) Numeric library
import matplotlib.pyplot as plt # (AUX) Graphics library

# Load input signal
fs, x = wavfile.read('./input/qC-G4-1-tu.wav') # Input signal 'x'

# Model parameters
h = daub(11) # Daubechies-11 low pass filter coefficients
g = qmf(h) # # Daubechies-11 high pass filter coefficients
P = 10 # Signal period (in number of samples)
N = 3 # Levels of wavelet decomposition

# Analysis step
a, b, cmfb = HBWT_Ana.hbwt(x, h, g, P, N)

# Synthesis step
y = HBWT_Synth.ihbwt(a, b, h, g) # reconstructed signal 'y'
wavfile.write('./output/synth_sig.wav', fs, y) # write WAV output file

### 5. GRAFICOS
t = np.arange(len(x))/float(fs) # Time vector (seconds)

# Power of input signal x[n] in dB
x_dB = 10*np.log10(x*x)
plt.figure(1)
plt.plot(t,x_dB)
plt.title('Signal x(t)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (dB)')

# DFT magnitude of x[n]
NFFT = 1024*32
X = np.fft.fftshift(np.fft.fft(x,NFFT))
Xmag = np.abs(X) #Spectra magnitude
fVals = fs*np.arange(-NFFT/2,NFFT/2)/NFFT
plt.figure()
plt.plot(fVals,Xmag)

# Spectrum magnitude of CMFB
NN = 1024 #DFT com NN pontos
CMFBa = np.fft.fftshift(np.fft.fft(cmfb[::-1,:],NN,axis=0)) #Espectro CMFB do banco de analise
CMFBamag = abs(CMFBa)
w = 2*np.pi*np.arange(-NN/2,NN/2)/NN #Frecuencia normalizada em rad

fig_cmfb = plt.figure()
ax = fig_cmfb.add_subplot(111)
ax.plot(w,CMFBamag)
ax.axis([0, np.pi, 0, 4])
ax.xaxis.grid(True)
ax.yaxis.grid(False)

unit   = 2*np.pi/P
x_tick = np.arange(0,np.pi+unit,unit) #Valores a mostrar no eixo x
x_label = [r"$0$", r"$\pi/7$", r"$2\pi/7$", r"$3\pi/7$", r"$4\pi/7}$", r"$5\pi/7$", r"$6\pi/7$", r"$\pi$"] #Etiqueta formatada para os valores do eixo x
ax.set_xticks(x_tick)
ax.set_xticklabels(x_label, fontsize=14)

plt.title('Banco de filtros Cosseno Modulado')
plt.xlabel('Frequencia normalizada')
plt.ylabel('Magnitude')
plt.show()

## Filtros H(z) e G(z)
fig_wavfil = plt.figure()
Cesc=np.fft.fftshift(np.fft.fft(g,NN));
Cwav=np.fft.fftshift(np.fft.fft(h,NN));
Cescmag=abs(Cesc); #Magnitude do espectro
Cwavmag=abs(Cwav);
w=2*np.pi*np.arange(-NN/2,NN/2)/NN; #Frequencia normalizada digital w
plt.plot(w,Cescmag,'b',w,Cwavmag,'m');

### TOCAR O SINAL
#!play test.wav
