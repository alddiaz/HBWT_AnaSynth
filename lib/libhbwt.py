# HBWT library
# Developed by Aldo Diaz
# University of Campinas, 2020

import numpy as np
from libfilt import *

# Discrete Wavelet Transform (DWT)
def dwt(x, h, g, N):
	# Input:
	# x: Input signal
	# h: Wavelet low pass wavelet filter coefficients
	# g: Wavelet high pass wavelet filter coefficients
	# N: Number of wavelet scales or "subbands"
	#
	# Output:
	# a: Wavelet (scale) decomposition coefficients
	# b: Wavelet (detail) decomposition coefficients

	L = len(h)-1
	h = h/np.linalg.norm(h)
	g = g/np.linalg.norm(g)
	a = np.empty((N, ), dtype=object)
	b = np.empty((N, ), dtype=object)

	for k in xrange(0, N):
		b[k] = upfirdn(g, x)
		b[k] = downsampling(b[k], 2, 1) # odd indexes
		x = upfirdn(h, x)
		x = downsampling(x, 2, 1) # odd indexes

	a[k] = x

	return a, b

# Cosine-Modulated Filter Bank (CMFB) using DCT-Type IV (DCT-IV) bases, a.k.a MDCT
def cmfb(x, P):
	# Input:
	# x: Input signal
	# P: Number of MDCT channels or "sidebands"
	#
	# Output:
	# y: P-channel filtered signal
	# w: MDCT filter coefficients

	k = np.arange(P)
	n = np.arange(2*P).reshape(-1, 1)
	hn = np.sin((k+0.5)*np.pi/2/P)
	h = np.hstack((hn, hn[::-1])).reshape(-1, 1)*np.ones(P)
	w = np.sqrt(2.0/P)*h*np.cos((2*n+P+1)*(2*k+1)*np.pi/4/P)
	y = upfirdn(w[::-1, :], x, 1, P)

	return y, w

# Harmonic Band Wavelet Transform (HBWT), as in [1, Section 2.2]
def hbwt(x, h, g, P, N):
	# Input:
	# x: Input signal
	# h: Wavelet low pass filter coefficients (e.g., Daubechies order 11)
	# g: Wavelet high pass filter coefficients (e.g., Daubechies order 11)
	# P: Number of MDCT channels or "sidebands" (matched to the period of 'x')
	# N: Number of wavelet scales or "subbands"
	#
	# Output:
	# a: Wavelet (scale) decomposition coefficients
	# b: Wavelet (detail) decomposition coefficients
	# w: MDCT filter coefficients

	y, w = cmfb(x, P)

	a = np.empty((N, P), dtype=object)
	b = np.empty((N, P), dtype=object)

	for k in xrange(0, P):
		a[:, k], b[:, k] = dwt(y[:, k], h, g, N)

	return a, b, w
