# HBWT_AnaSynth
Implementation of the Harmonic Band Wavelet Transform (HBWT) in Python.<br />
Analysis and Synthesis modules are provided as separate functions.

**Please cite this paper and code if you use HBWT_AnaSynth in your research:**<br />
[1] Díaz Salazar, Aldo André and Mendes, Rafael, "Analysis/Synthesis Of The Andean Quena Via Harmonic Band Wavelet Transform", In: Proceedings of the 18th International Conference on Digital Audio Effects (DAFx-15), 2015, pp. 1–4.<br />
https://www.ntnu.edu/documents/1001201110/1266017954/DAFx-15_submission_74_v3.pdf
<br />
[2] Díaz Salazar, Aldo André, "HBWT_AnaSynth", Campinas, Brazil, 2015.
<br /><br />
N.B.: Only files in **16-bit PCM** WAV format are supported

# Methods
You will work with two functions called "hbwt" and "ihbwt" as follows:

1. From **libhbwt.py** file (the direct HBWT transform, as in Section 2.2 in [1]) you will find the function **hbwt(x, h, g, P, N)**, where:<br />
x: input signal x(n)<br />
h: low pass wavelet filter coefficients (typically, a Daubechies wavelet filter of order 11).<br />
g: high pass wavelet filter coefficients (typically, a Daubechies wavelet filter of order 11).<br />
P: the number of MDCT channels or "sidebands" (typically adjusted to match the period of input signal x(n) )<br />
N: the number of wavelet scales or "subbands".<br />

2. From **libhibwt.py** file (the inverse HBWT transform, as in Section 2.3 in [1]) you will find the function **ihbwt(a, b, h, g)**, where:<br />
a: wavelet filter coefficients called "scale residue" at scale N per channel p (see Eq. (7) in [1])<br />
b: wavelet filter coefficients called "expansion coefficients" at scales n per channel p (see Eq. (7) in [1])<br />
h: low pass wavelet filter coefficients (the same used in Step 1).<br />
g: high pass wavelet filter coefficients (the same used in Step 1)<br />

# Reference
[1] A. A. Díaz Salazar, R. S. Mendes, "**Analysis/Synthesis Of The Andean Quena Via Harmonic Band Wavelet Transform**", In: Proceedings of the 18th International Conference on Digital Audio Effects (DAFx-15), 2015, pp. 1–4.<br />
https://www.ntnu.edu/documents/1001201110/1266017954/DAFx-15_submission_74_v3.pdf <br />
[2] A. A. Díaz Salazar, "HBWT_AnaSynth", Campinas, Brazil, 2015. <br />
[3] P. Polotti, G. Evangelista, "**Fractal Additive Synthesis via Harmonic-Band Wavelets**", In: Computer Music Journal, vol.25, no. 3, pp. 22–37, Mar. 2001.
