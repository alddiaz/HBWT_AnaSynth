# Fundamental frequency estimation (pitch estimation)
# N.B.: It computes the harmonic of highest amplitude (might be biased!)
#
# Developed by Aldo Diaz
# University of Campinas, 2020

import numpy as np # numeric library
import operator as operator

def estimatef0(x, fs):
	# Input:
	# x: Input signal
	# fs: Sampling frequency
	#
	# Output:
	# f0: Estimated fundamental frequency
	# P: Estimated period

	# 1. Determining the DFT point resolution
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
	index, value = max(enumerate(abs(X)), key = operator.itemgetter(1)) # index: Highest frequency position
	f0	= fVals[index] # Estimated fundamental frequency (pitch estimation)
	P	= int(np.round(fs/f0)) # Signal's period P (in number of samples)

	return f0, P
