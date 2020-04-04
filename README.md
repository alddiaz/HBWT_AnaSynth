# HBWT_AnaSynth
Python implementation of the Harmonic Band Wavelet Transform (HBWT).<br />
**N.B.:** Only **WAV format** files are supported!

**Please cite these paper and software if you use HBWT_AnaSynth in your research:**<br />
[1] A. A. Díaz Salazar, R. S. Mendes, "Analysis/Synthesis Of The Andean Quena Via Harmonic Band Wavelet Transform", In: Proceedings of the 18th International Conference on Digital Audio Effects (DAFx-15), 2015, pp. 1–4.<br />
https://www.ntnu.edu/documents/1001201110/1266017954/DAFx-15_submission_74_v3.pdf
<br />
[2] A. A. Díaz Salazar, "HBWT_AnaSynth", Campinas, Brazil, 2015.

# Example
Read **example.py**.

> import lib.libhbwt as HBWT_Ana # HBWT Analysis
import lib.libihbwt as HBWT_Synth # HBWT Synthesis
from scipy.signal import daub, qmf # Daubechies wavelets
from scipy.io import wavfile # WAV files
from lib.float32 import * # 'float32' input data normalization
from lib.estimatef0 import * # fundamental frequency estimation

> # Load input signal
fs, x = wavfile.read('./input/qC-G4-1-tu.wav') # input signal 'x'
x, data_type = float32(x) # data normalization

> # Model parameters
h     = daub(11) # Daubechies-11 low pass filter coefficients
g     = qmf(h) # Daubechies-11 high pass filter coefficients
f0, P = estimatef0(x, fs) # f0: estimated fundamental frequency of input signal 'x' (Hertz)
                          # P: estimated (integer) signal period (given in number of samples)
N = 5 # levels of wavelet decomposition

> # Analysis step
a, b, cmfb = HBWT_Ana.hbwt(x, h, g, P, N)

> # Synthesis step
y = HBWT_Synth.ihbwt(a, b, h, g) # reconstructed signal 'y'
y = ifloat32(x, data_type) # Data back normalization
wavfile.write('./output/synth_sig.wav', fs, y) # write WAV output file

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
