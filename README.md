# HBWT_AnaSynth
Python implementation of the Harmonic Band Wavelet Transform (HBWT).<br />
**N.B.:** Only files **WAV format** is supported!

**Please cite these paper and software if you use HBWT_AnaSynth in your research:**<br />
[1] A. A. Díaz Salazar, R. S. Mendes, "Analysis/Synthesis Of The Andean Quena Via Harmonic Band Wavelet Transform", In: Proceedings of the 18th International Conference on Digital Audio Effects (DAFx-15), 2015, pp. 1–4.<br />
https://www.ntnu.edu/documents/1001201110/1266017954/DAFx-15_submission_74_v3.pdf
<br />
[2] A. A. Díaz Salazar, "HBWT_AnaSynth", Campinas, Brazil, 2015.

# Methods
- Analysis step
1. From **libhbwt.py** file (the direct HBWT transform, as in Section 2.2 in [1]) you will find the function **hbwt(x, h, g, P, N)**, where:<br />
x: Input signal x[n]<br />
h: Low pass wavelet filter coefficients (e.g., Daubechies order 11).<br />
g: High pass wavelet filter coefficients (e.g., Daubechies order 11).<br />
P: Number of MDCT channels or "sidebands" (matched to the period of input signal x[n]).<br />
N: Number of wavelet scales or "subbands".<br />

- Synthesis step
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
