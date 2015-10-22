#Biblioteca de funcoes para o calculo da inversa HBWT
#Desenvolvida por Aldo Diaz
#Universidade Estadual de Campinas, 2015

import numpy as np
import scipy.signal as signal
from libfilt import* #Biblioteca de filtragem

#Funcao que calcula a inversa da Transformada Wavelet
#dados os coeficientes de escala a_k[n] e Wavelet b_k[n]
def iwt(a, b, h, g):
	#a: Coeficientes de escala
	#b: Coeficientes Wavelet
	#h: Filtro de escala
	#g: Filtro Wavelet

	h = h[::-1]/np.linalg.norm(h) #Fornece o filtro anticausal h[n] de sintese
	g = g[::-1]/np.linalg.norm(g) #Fornece o filtro anticausal g[n] de sintese
	L = len(h)-1
	N = len(a)-1 #Numero de niveis de analise Wavelet
	aa = a[N] #Utilisa-se somente os coeficientes da escala mais alta
	
	for k in xrange(N, -1, -1): # Conta de M ate 0
		bb = b[k]
		Lbb = len(bb)
		Laa = len(aa)
		if Lbb > Laa:
			bb = bb[0:Laa]
		bb = expansao(bb,2) #Superamostragem
		bb = signal.lfilter(g,1,bb) #Filtragem
		if Laa > Lbb:
			aa = aa[0:Lbb]
		aa = expansao(aa,2) #Superamostragem
		aa = signal.lfilter(h,1,aa) #Filtragem
		aa = aa + bb #Somo para a seguinte etapa
		aa = aa[L-1:] #Descarta zeros redundates
	
	return aa

#Funcao que para calculo do banco de filtros CMFB
def icmfb(x, P):
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
	y = exp_fir_diz(x[:,0], w[:,0], P, 1) # Primeira expansao e filtragem
	
	y = y[2*P-1:]
	
	for k in xrange(1,P):
		yy = exp_fir_diz(x[:,k], w[:,k], P, 1)
		y = yy[2*P-1:]+y
	
	return y, w

#Funcao que calcula a HBWT
def ihbwt(a, b, h, g):
	# ENTRADAS:
	#a: Matriz de coeficientes de escala
	#b: Matriz de coeficientes Wavelet
	#h: Filtro de sintese passa-baixa (escala)
	#g: Filtro de sintese passa-alta (Wavelet)
	
	# SAIDAS:
	#x: Sinal reconstruido
	
	P = len(a[0]) #Colunas de 'a' igual ao periodo 'P' de 'x'
	temp = iwt(a[:,0], b[:,0], h, g) #Primera inversa WT
	N = temp.size #Numero de filas (Niveis de analise)
	aa = np.empty((N,P),dtype=object)
	aa[:,0] = temp
	
	for k in xrange(1,P):
		aa[:,k] = iwt(a[:,k], b[:,k], h, g)
	
	[x, w] = icmfb(aa, P)

	return x
