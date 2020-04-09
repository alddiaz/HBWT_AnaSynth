# Inverse HBWT library
# Developed by Aldo Diaz
# University of Campinas, 2020

import numpy as np
from libfilt import *

# Inverse Discrete Wavelet Transform (IDWT)
def idwt(a, b, h, g):
	# Input:
	# a: Wavelet "scale residue" coefficients
	# b: Wavelet "expansion " coefficients
	# h: wavelet low pass filter coefficients
	# g: Wavelet high pass filter coefficients
	#
	# Output:
	# y: Reconstructed signal

	h = h[::-1]/np.linalg.norm(h)
	g = g[::-1]/np.linalg.norm(g)
	L = len(h)-1
	N = len(a)-1
	aa = a[N]

	for k in xrange(N, -1, -1):
		bb = b[k]
		Lbb = len(bb)
		Laa = len(aa)
		if Lbb > Laa:
			bb = bb[0:Laa]
		bb = upfirdn(g, bb, 2)
		if Laa > Lbb:
			aa = aa[0:Lbb]
		aa = upfirdn(h, aa, 2)
		aa = aa + bb
		aa = aa[L-1:]

	y = aa

	return y

# Inverse Cosine-Modulated Filter Bank (ICMFB) using DCT-Type IV (DCT-IV) bases, a.k.a IMDCT
def icmfb(y, P):
	# Input:
	# y: Input signal
	# P: Number of IMDCT channels or "sidebands"
	#
	# Output:
	# x: Reconstructed signal
	# w: IMDCT filter coefficients

	k = np.arange(P)
	n = np.arange(2*P).reshape(-1, 1)
	hn = np.sin((k+0.5)*np.pi/2/P)
	hn = np.hstack((hn, hn[::-1])).reshape(-1, 1)
	h = hn*np.ones(P)
	w = np.sqrt(2.0/P)*h*np.cos((2*n+P+1)*(2*k+1)*np.pi/4/P)

	x = 0
	for k in xrange(0, P):
		xx = upfirdn(w[:, k], y[:, k], P, 1)
		x = xx[2*P-1:] + x

	return x, w

# Inverse Harmonic Band Wavelet Transform, as in [1, Section 2.3]
def ihbwt(a, b, h, g):
	# Input:
	# a: Wavelet "scale residue" coefficients at scale N per channel p (see Eq. (7) in [1])
	# b: Wavelet "expansion " coefficients at scales n per channel p (see Eq. (7) in [1])
	# h: Wavelet low pass filter coefficients
	# g: Wavelet high pass filter coefficients
	#
	# Output:
	# x: Reconstructed signal
	# w: IMDCT filter coefficients

	P = len(a[0])
	y = idwt(a[:,0], b[:,0], h, g)
	N = len(y)
	aa = np.empty((N, P))
	aa[:,0] = y

	for k in xrange(1, P):
		aa[:, k] = idwt(a[:, k], b[:, k], h, g)

	x, w = icmfb(aa, P)

	return x
