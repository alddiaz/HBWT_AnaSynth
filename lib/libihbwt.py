# HBWT library
# Developed by Aldo Diaz
# University of Campinas, 2015

import numpy as np
import scipy.signal as signal
from libfilt import*

# Inverse Discrete Wavelet Transform (IDWT)
def idwt(a, b, h, g):
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
		bb = upsampling(bb, 2)
		bb = signal.lfilter(g, 1, bb)
		if Laa > Lbb:
			aa = aa[0:Lbb]
		aa = upsampling(aa, 2)
		aa = signal.lfilter(h, 1, aa)
		y = aa + bb
		y = y[L-1:]

	return y

# Inverse Cosine-Modulated Filter Bank (ICMFB)
def icmfb(y, P):
	# Output:
	# x: Reconstructed signal
	# w: IMDCT filter coefficients

	k = np.arange(P)
	n = np.arange(2*P).reshape(-1, 1)
	hn = np.sin((k+0.5)*np.pi/2/P)
	hn = np.hstack((hn, hn[::-1])).reshape(-1, 1)
	h = hn*np.ones(P)
	w = np.sqrt(2.0/P)*h*np.cos((2*n+P+1)*(2*k+1)*np.pi/4/P)
	x = up_fir_down(y[:,0], w[:,0], P, 1)

	x = x[2*P-1:]

	for k in xrange(1, P):
		xx = up_fir_down(y[:,k], w[:,k], P, 1)
		x = xx[2*P-1:] + x

	return x, w

# Inverse Harmonic Band Wavelet Transform
def ihbwt(a, b, h, g):
	# Output:
	# x: Reconstructed signal
	# w: IMDCT filter coefficients

	P = len(a[0])
	y = idwt(a[:,0], b[:,0], h, g)
	N = y.size
	aa = np.empty((N,P), dtype=object)
	aa[:,0] = y

	for k in xrange(1, P):
		aa[:,k] = idwt(a[:,k], b[:,k], h, g)

	x, w = icmfb(aa, P)

	return x
