# Inverse HBWT library
# Developed by Aldo Diaz
# University of Campinas, 2020

import numpy as np
import scipy.signal as signal
from libfilt import*

# Discrete Wavelet Transform (DWT)
def dwt(x, h, g, N):
	# Output:
	# a: Wavelet (scale) decomposition coefficients
	# b: Wavelet (detail) decomposition coefficients

	L = len(h)-1
	h = h/np.linalg.norm(h)
	g = g/np.linalg.norm(g)
	a = np.empty((N, ), dtype=object)
	b = np.empty((N, ), dtype=object)

	for k in xrange(0, N):
		x = np.append(x, np.zeros(L))
		bb = signal.lfilter(g, 1, x)
		bb = downsampling(bb, 2, 1) # odd indexes
		b[k] = bb
		x = signal.lfilter(h, 1, x)
		x = downsampling(x, 2, 1) # odd indexes

	a[k] = x

	return a, b

# Cosine-Modulated Filter Bank (CMFB) using DCT-Type IV (DCT-IV) bases, a.k.a MDCT
def cmfb(x, P):
	# Output:
	# y: P-channel filtered signal
	# w: MDCT filter coefficients

	k = np.arange(P)
	n = np.arange(2*P).reshape(-1, 1)
	hn = np.sin((k+0.5)*np.pi/2/P)
	hn = np.hstack((hn, hn[::-1])).reshape(-1, 1)
	h = hn*np.ones(P)
	w = np.sqrt(2.0/P)*h*np.cos((2*n+P+1)*(2*k+1)*np.pi/4/P)
	y = up_fir_down(x, w[::-1, :], 1, P)

	return y, w

# Harmonic Band Wavelet Transform (HBWT)
def hbwt(x, h, g, P, N):
	# The direct HBWT transform, as in [1, Section 2.2]
	#
	# Input:
	# x: Input signal
	# h: Low pass wavelet filter coefficients (e.g., Daubechies order 11)
	# g: High pass wavelet filter coefficients (e.g., Daubechies order 11)
	# P: Number of MDCT channels or "sidebands" (matched to the period of 'x')
	# N: Number of wavelet scales or "subbands"
	#
	# Output:
	# a: Wavelet (scale) decomposition coefficients
	# b: Wavelet (detail) decomposition coefficients
	# w: MDCT filter coefficients

	x, w = cmfb(x, P)
	a = np.empty((N, P), dtype=object)
	b = np.empty((N, P), dtype=object)

	for k in xrange(0,P):
		a[:, k], b[:, k] = dwt(x[:, k], h, g, N)

	return a, b, w
