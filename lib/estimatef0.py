# Fundamental frequency estimation
# Developed by Aldo Diaz
# University of Campinas, 2015

import numpy as np # numeric library
import operator as operator

def estimatef0(x, fs):
	## f0 estimation
	# Input:
	# x: input signal
	# fs: sampling frequency
	#
	# Output:
	# f0: estimated fundamental frequency

	# 1.  Determining the number of DFT points
	j 	= 1
	NN	= 1
	while(x.size > NN):
		if(x.size/NN) != 0:
			j	= j+1
			NN	= pow(2, j)

	# 2. DFT calculation
	X		= np.fft.fft(x, NN)
	X		= X[0:NN/2]
	fVals	= np.linspace(0, fs/2, NN/2) # frequency vector (Hz)

	# 3. Signal period estimation
	index, value = max(enumerate(abs(X)), key = operator.itemgetter(1))
	f0	= fVals[index] #index: Posicao da maior frequencia
	P	= int(np.round(fs/f0)) #Estimacao de P em numero de amostras

	return f0, P
