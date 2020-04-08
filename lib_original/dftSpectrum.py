# DFT magnitue spectrum calculation
# Developed by Aldo Diaz
# University of Campinas, 2020

import numpy as np # numeric library

def dftSpectrum(x, NFFT, AXIS=0):
    # Input:
    # x: Input Signal
    # NFFT: Number of FFT points
    # AXIS: Axis over which to compute the FFT
    #
    # Output:
    # Xmag: FFT magnitude spectrum
    # omega: Normalized frequency (radians)

    if len(x.shape) == 1: # 1-D signal
        X       = np.fft.fftshift(np.fft.fft(x, NFFT))
    elif len(x.shape) == 2: # Array signal
        X       = np.fft.fftshift(np.fft.fft(x, NFFT, axis=AXIS))

    Xmag    = np.abs(X[NFFT/2:]) # DFT spectrum
    omega   = 2*np.pi*np.arange(NFFT/2)/NFFT # Normalized frequency

    return Xmag, omega
