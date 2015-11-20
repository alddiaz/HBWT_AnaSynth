#Biblioteca de funcoes para o calculo da HBWT
#Desenvolvida por Aldo Diaz
#Universidade Estadual de Campinas, 2015

import numpy as np
import scipy.signal as signal
from libfilt import* #Biblioteca de filtragem

def wt(x, h, g, N):
	L = h.size-1
	h = h/np.linalg.norm(h)
	g = g/np.linalg.norm(g)
	a = np.empty((N,),dtype=object)
	b = np.empty((N,),dtype=object)

	for k in xrange(0,N):
		x = np.append(x,np.zeros(L))
		bb = signal.lfilter(g, 1, x)
		bb = bb[1::2]
		b[k] = bb
		x = signal.lfilter(h, 1, x)
		x = x[1::2]
	
	a[k] = x
	
	return a, b

def cmfb(x, P):
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
	y = exp_fir_diz(x, w[::-1,:], 1, P)

	return y, w

def hbwt(x, h, g, P, N):
	[x, w] = cmfb(x, P)
	a = np.empty((N,P),dtype=object)
	b = np.empty((N,P),dtype=object)

	for k in xrange(0,P):
		[a[:,k], b[:,k]] = wt(x[:,k], h, g, N)

	return a, b, w
