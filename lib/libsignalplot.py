# Plot DWT magnitude spectrum
# Developed by Aldo Diaz
# University of Campinas, 2020

import numpy as np # numeric library
import matplotlib.pyplot as plt # graphics library
from lib.dftSpectrum import * # DFT magnitue spectrum

def plotSignal(x, y, fs=1):
    # Input:
    # x: Input signal
    # y: Reconstructed signal
    # fs: Sampling Frequency

    tx = np.arange(len(x))/float(fs) # time vector (seconds)
    ty = np.arange(len(y))/float(fs) # time vector (seconds)
    plt.figure()
    plt.subplot(211)
    plt.plot(tx, x, 'b')
    plt.xlim([ 0, tx.max() ]) # limited number of harmonics
    plt.ylabel('Amplitude')
    plt.title('Input signal x(t)')
    plt.subplot(212)
    plt.plot(ty, y, 'm')
    plt.xlim([ 0, ty.max() ]) # limited number of harmonics
    plt.title('Reconstructed signal y(t)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.tight_layout()

def plotSignalSpectrum(x, NFFT, f0, k=5, fs=1, scale='mag'):
    # Input:
    # x: signal
    # NFFT: Number of DWT points
    # f0: fundamental frequency
    # k: Number of harmonics
    # fs: Fundamental frequency
    # scale: Magnitude in DB

    Xmag, omega = dftSpectrum(x, NFFT) # DFT spectrum
    Xmag = 20*np.log10(Xmag) if scale == 'dB' else Xmag # scale adjust
    fVals       = fs*omega/2/np.pi # frequency in Hertz
    NF0 = int(fVals[-1]/f0) # Number of harmonics
    fig_dft     = plt.figure()
    ax          = fig_dft.add_subplot(111)
    x_tick      = f0*np.arange(0, NF0) # x axis labels
    x_label     = [ r"$0$", r"$f_{0}$" ]
    x_label.extend([ r"$"+str(i)+"f_{0}$" for i in range(2, NF0-1) ])
    plt.plot(fVals, Xmag, 'b')
    ax.set_xticks(x_tick)
    ax.set_xticklabels(x_label, fontsize=10)
    plt.xlim([ 0, k*f0 ]) # limited number of harmonics
    ax.xaxis.grid(True)
    plt.title('Signal spectrum, f0 = '+str(round(f0, 1))+' Hz')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)' if scale == 'dB' else 'Magnitude')
    plt.tight_layout()

def plotCMFBSpectrum(cmfb, NFFT, P, k, scale='mag'):
    # Input:
    # cmfb: CMFB filter coefficients
    # NFFT: Number of DWT points
    # P: Signal period
    # k: Number of harmonics
    # scale: Magnitude in DB

    CMFBmag, omega = dftSpectrum(cmfb, NFFT) # CMFB spectrum
    CMFBmag = np.log10(CMFBmag)/np.log10(np.sqrt(P)) if scale == 'dB' else CMFBmag/np.sqrt(P) # scale adjust
    fig_cmfb       = plt.figure()
    ax             = fig_cmfb.add_subplot(111)
    x_tick         = np.pi*np.arange(0, P+1)/P # x axis labels
    x_label        = [ r"$0$", r"$\frac{\pi}{"+str(P)+"}$" ]
    x_label.extend([ r"$\frac{"+str(i)+"\pi}{"+str(P)+"}$" for i in range(2, P) ])
    x_label.extend([ r"$\pi$" ])
    ax.plot(omega, CMFBmag)
    ax.set_xticks(x_tick)
    ax.set_xticklabels(x_label, fontsize=10)
    ax.axis([ 0, 2*k*np.pi/P, 0, 1.1*CMFBmag.max() ]) # limited spectrum
    ax.xaxis.grid(True)
    plt.title('Cosine-Modulated Filter Bank spectrum, P = '+str(P)+' channels')
    plt.xlabel('Normalized frequency (rad)')
    plt.ylabel('Magnitude (dB)' if scale == 'dB' else 'Magnitude')
    plt.tight_layout()

def plotDWTSpectrum(h, g, NFFT, scale='mag'):
    # Input:
    # h: DWT low pass filter coefficients
    # g: DWT high pass filter coefficients
    # NFFT: Number of DFT points
    # scale: Magnitude in DB

    DWTlomag, omega = dftSpectrum(h, NFFT) # DWT low pass filter
    DWThimag, _ = dftSpectrum(g, NFFT) # DWT high pass filter
    DWTlomag = np.log10(DWTlomag)/np.log10(np.sqrt(2)) if scale == 'dB' else DWTlomag/np.sqrt(2) # scale adjust
    DWThimag = np.log10(DWThimag)/np.log10(np.sqrt(2)) if scale == 'dB' else DWThimag/np.sqrt(2) # scale adjust
    fig_dwt     = plt.figure()
    ax          = fig_dwt.add_subplot(111)
    x_tick      = np.pi*np.arange(0, 5)/4 # x axis labels
    x_label     = [ r"$0$", r"$\frac{\pi}{4}$", r"$\frac{\pi}{2}$", r"$\frac{3\pi}{4}$", r"$\pi$" ]
    plt.plot(omega, DWTlomag, 'b', omega, DWThimag, 'm')
    ax.set_xticks(x_tick)
    ax.set_xticklabels(x_label, fontsize=10)
    ax.axis([ 0, np.pi, 0, 1.1*DWTlomag.max() ]) # limited spectrum
    ax.legend([ 'H(z)', 'G(z)' ], loc='upper right')
    ax.xaxis.grid(True)
    plt.title('Discrete Wavelet Transform spectrum, Daubechies-11 filters')
    plt.xlabel('Normalized frequency (rad)')
    plt.ylabel('Magnitude (dB)' if scale == 'dB' else 'Magnitude')
    plt.tight_layout()
