# HBWT library
# Developed by Aldo Diaz
# University of Campinas, 2015

import numpy as np
import scipy.signal as signal
from libfilt import*

# Inverse Discrete Wavelet Transform (IDWT)
def iwt(a, b, h, g):
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
		bb = upsampling(bb,2)
		bb = signal.lfilter(g,1,bb)
		if Laa > Lbb:
			aa = aa[0:Lbb]
		aa = upsampling(aa,2)
		aa = signal.lfilter(h,1,aa)
		aa = aa + bb
		aa = aa[L-1:]

	return aa

# Inverse Cosine-Modulated Filter Bank (ICMFB)
def icmfb(x, P):
	k = np.arange(P)
	n = np.arange(2*P)
	n.shape = (-1,1)
	hn = np.sin((k+.5)*np.pi/2/P)
	hn = np.hstack((hn,hn[::-1]))
	hn.shape = (-1,1)
	h = hn*np.ones(P)
	argum = (2*n+P+1)*(2*k+1)*np.pi/4/P
 	coss = np.cos(argum)
	w = np.sqrt(2.0/P)*h*coss
	y = up_fir_down(x[:,0], w[:,0], P, 1)

	y = y[2*P-1:]

	for k in xrange(1,P):
		yy = up_fir_down(x[:,k], w[:,k], P, 1)
		y = yy[2*P-1:]+y

	return y, w

# Inverse Harmonic Band Wavelet Transform
def ihbwt(a, b, h, g):
	P = len(a[0])
	temp = iwt(a[:,0], b[:,0], h, g)
	N = temp.size
	aa = np.empty((N,P),dtype=object)
	aa[:,0] = temp

	for k in xrange(1,P):
		aa[:,k] = iwt(a[:,k], b[:,k], h, g)

	[x, w] = icmfb(aa, P)

	return x
