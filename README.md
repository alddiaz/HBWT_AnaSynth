# HBWT_AnaSynth
Implementation of the Harmonic Band Wavelet Transform (HBWT) in Python.
Analysis and Synthesis provided as separate functions.

You will work with two functions called "hbwt" and "ihbwt" as follows:

1. From libhbwt.py file (the direct HBWT transform, as in Section 2.2 in [1]) you will find the function hbwt(x, h, g, P, N), where:
x: input signal x(n)
h: low pass wavelet filter coefficients (typically, a Daubechies wavelet filter of order 11).
g: high pass wavelet filter coefficients (typically, a Daubechies wavelet filter of order 11).
P: the number of MDCT channels or "sidebands" (typically adjusted to match the period of input signal x(n) )
N: the number of wavelet scales or "subbands".

2. From libhibwt.py file (the inverse HBWT transform, as in Section 2.3 in [1]) you will find the function ihbwt(a, b, h, g), where:
a: wavelet filter coefficients called "scale residue" at scale N per channel p (see Eq. (7) in [1])
b: wavelet filter coefficients called "expansion coefficients" at scales n per channel p (see Eq. (7) in [1])
h: low pass wavelet filter coefficients (the same used in Step 1).
g: high pass wavelet filter coefficients (the same used in Step 1)

# Reference
[1] A. Díaz and R. Mendes, “Analysis/Synthesis Of The Andean Quena Via Harmonic Band Wavelet Transform,” in Proceedings of the 18th International Conference on Digital Audio Effects (DAFx-15), 2015, pp. 1–4.
https://www.ntnu.edu/documents/1001201110/1266017954/DAFx-15_submission_74_v3.pdf

[2] P. Polotti and G. Evangelista, Fractal Additive Synthesis via Harmonic-Band Wavelets, In: Computer Music Journal , vol.25, no. 3, pp. 22–37, Mar. 2001.
