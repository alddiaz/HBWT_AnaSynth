# Filtering library
# Developed by Aldo Diaz
# University of Campinas, 2015

from numpy import empty, zeros, convolve

# Upsampling
def upsampling(x, L):
	# x: Input signal
	# L: Upsampling factor

	l = len(x)*L
	y = zeros(l)
	y[::L] = x
	return y

# Downsampling
def downsampling(x, M):
	# x: Input signal
	# M: Downsampling factor

	y = x[0::M] # Downsampling using even indexes
	return y

# Upsampling -> FIR Filtering -> Downsampling
def up_fir_down(x, h, L, M):
	# x: Input signal
	# h: Filtering matrix. The columns contain the coefficients of the impulse response of each filter h_k[n]
	# L: Upsampling factor
	# M: Downsampling factor

	if L != 1: # Synthesis step
		y = upsampling(x, L) # Upsampling x in a factor L
		A = convolve(y, h) # Convolution
		A = A[:len(A)-(L-1)] # Prune ending zeros
	else: # Analysis step
		y = x
		temp = convolve(y, h[:,0]) # First convolution
		NC = len(h[0]) # Number of h columns
		NF = temp.size # Size of the convolution vector
		A = empty((NF,NC)) # Allocate matrix A
		A[:,0] = temp # Store the first convolution
		for k in xrange(1,NC):
			A[:,k] = convolve(y, h[:,k])
	if M != 1:
		A = downsampling(A, M) # Downsampling A in factor M
	return A
