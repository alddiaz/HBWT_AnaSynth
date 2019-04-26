#Biblioteca de funcoes para filtragem
#Desenvolvida por Aldo Diaz
#Universidade Estadual de Campinas, 2015

from numpy import empty,zeros,convolve

#Funcao Expansor
def expansao(x, L):
	#x: Sinal de entrada
	#L: Fator de interpolacao
	
	l = len(x)*L
	y = zeros(l)
	y[::L] = x
	return y

#Funcao Dizimador
def dizimacao(x, M):
	#x: Sinal de entrada
	#M: Fator de dizimacao
	
	y = x[0::M] #VERIFICAR SE SAO PARES OU IMPARES
	return y

#Funcao Expansao-FiltragemFIR-Dizimacao
def exp_fir_diz(x, h, L, M):
	#x: Sinal de entrada
	#h: Matriz de filtragem. Cada coluna contem os coeficientes da respota ao impulso de cada filtro h_k[n]
	#L: Fator de interpolacao
	#M: Fator de dizimacao
	
	if L != 1: #Etapa de sintese
		y = expansao(x, L) #Expansao de x em fator L
		A = convolve(y, h) #Convolucao
		A = A[:len(A)-(L-1)] #Descarta zeros no final
	else: #Etapa de analise
		y = x
		temp = convolve(y, h[:,0]) #Primeira convolucao
		NC = len(h[0]) #Numero de colunas de h
		NF = temp.size #Tamanho do vetor convolucao	
		A = empty((NF,NC)) #Dimensiona a matriz A
		A[:,0] = temp #Armazena a primeira convolucao
		
		for k in xrange(1,NC):
			A[:,k] = convolve(y, h[:,k])
	
	if M != 1:
		A = dizimacao(A, M) #Dizimacao de A em fator M
	return A

