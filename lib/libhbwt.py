#Biblioteca de funcoes para o calculo da HBWT
#Desenvolvida por Aldo Diaz
#Universidade Estadual de Campinas, 2015

import numpy as np
import scipy.signal as signal
from libfilt import* #Biblioteca de filtragem

#Funcao que calcula a Transformada Wavelet
#dada a resposta ao impulso dos filtros Wavelet H(z) e G(z)
#e o nivel de profundidade da analise
def wt(x, h, g, N):
	#x: Sinal de entrada
	#h: Filtro de escala
	#g: Filtro Wavelet
	#N: Niveis de profundidade na analise Wavelet

	L = h.size-1
	h = h/np.linalg.norm(h)
	g = g/np.linalg.norm(g)
	a = np.empty((N,),dtype=object)
	b = np.empty((N,),dtype=object)

	for k in xrange(0,N):    # Conta de 0 ate (M-1)
		x = np.append(x,np.zeros(L)) # Zero-padding
		bb = signal.lfilter(g, 1, x) # Filtragem g[n] wavelet
		bb = bb[1::2]          # Decimacao fator 2 das amostras impares
		b[k] = bb              # Coeficientes wavelet
		x = signal.lfilter(h, 1, x) # Filtragem h[n] escala
		x = x[1::2]          # Decimacao fator 2 das amostras impares
	
	a[k] = x                     # Coeficientes de escala
	
	return a, b

#Funcao que para calculo do banco de filtros CMFB
def cmfb(x, P):
	#x: Sinal de entrada
	#P: Numero de bancos

	k = np.arange(P) #Numero de canais do banco
	n = np.arange(2*P) #Tamanho dos filtros em amostras
	n.shape = (-1,1) #Fazendo 'n' um vetor coluna
	hn = np.sin((k+.5)*np.pi/2/P) #Janela seno h[n]
	hn = np.hstack((hn,hn[::-1])) #Condicao de simetria
	hn.shape = (-1,1) #Fazendo 'hk' um vetor coluna
	h = hn*np.ones(P) #Matriz de ordem 2PxP
	argum = (2*n+P+1)*(2*k+1)*np.pi/4/P #Argumento do cosseno
 	coss = np.cos(argum)
	w = np.sqrt(2.0/P)*h*coss #Gera a matriz de filtragem CMFB
				    #Operador (*) e o produto elemento a elemento
	y = exp_fir_diz(x, w[::-1,:], 1, P) # Filtragem e decimacao
	#w[::-1,:]: Banco de analise (Reversao no tempo do Banco de sintese, mas tem resposta em frequencia identica)

	return y, w

#Funcao que calcula a HBWT
def hbwt(x, h, g, P, N):
	# ENTRADAS:
	#x: Sinal de entrada
	#h: Filtro de analise passa-baixa (escala)
	#g: Filtro de analise passa-alta (Wavelet)
	#P: Periodo do sinal x em numero de amostras
	#N: Niveis de profundidade na analise Wavelet
	
	# SAIDAS:
	# a: matriz de coeficientes de escala
	# b: matriz de coeficientes wavelet
	# cmfb: matriz de filtragem CMFB
	
	[x, w] = cmfb(x, P) #Divisao em sub-bandas usando MDCT (DCT-IV)
	a = np.empty((N,P),dtype=object)
	b = np.empty((N,P),dtype=object)

	for k in xrange(0,P):
		[a[:,k], b[:,k]] = wt(x[:,k], h, g, N)

	return a, b, w
