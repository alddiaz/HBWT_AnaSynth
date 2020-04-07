# HBWT_AnaSynth
Python implementation of the Harmonic Band Wavelet Transform (HBWT).<br />
**N.B.:** Only **WAV format** files are supported!

**Please cite these works and software if you use HBWT_AnaSynth in your research:**<br />
[1] A. A. Díaz Salazar, R. S. Mendes, "Analysis/Synthesis Of The Andean Quena Via Harmonic Band Wavelet Transform", In: Proceedings of the 18th International Conference on Digital Audio Effects (DAFx-15), 2015, pp. 1–4. [Online](https://www.ntnu.edu/documents/1001201110/1266017954/DAFx-15_submission_74_v3.pdf).<br />
[2] A. A. Díaz Salazar, "HBWT_AnaSynth", Campinas, Brazil, 2015. <br />
[3] A. A. Díaz Salazar, “Analysis of musical instruments via the Harmonic Band Hurst Exponent: Comparative study of the Quena and other wind instruments” (in Portuguese), University of Campinas, 2015. [Online](http://repositorio.unicamp.br/handle/REPOSIP/259746).

# Example
Run <**example.py**>.
```python
import lib.libhbwt as HBWT_Ana # HBWT Analysis
import lib.libihbwt as HBWT_Synth # HBWT Synthesis
from scipy.signal import daub, qmf # Daubechies wavelets
from scipy.io import wavfile # WAV files
from lib.float32 import * # 'float32' input data type normalization
from lib.estimatef0 import * # fundamental frequency estimation

# Load input signal
filename = 'quena_G4'
fs, x = wavfile.read('./input/'+filename+'.wav') # input signal 'x'
xn, data_type = float32(x) # data type normalization
# Model parameters
h     = daub(11) # Daubechies-11 low pass filter coefficients
g     = qmf(h) # Daubechies-11 high pass filter coefficients
f0, P = estimatef0(xn, fs) # f0: fundamental frequency (Hz), P: signal period (in number of samples)
N     = 5 # levels of wavelet decomposition
# Analysis step
a, b, w = HBWT_Ana.hbwt(xn, h, g, P, N) # HBWT decomposition coefficients 'a' and 'b' and CMFB filter bank 'w'
# Synthesis step
yn = HBWT_Synth.ihbwt(a, b, h, g) # reconstructed signal 'y'
# Write ouput signal
yn = yn[:len(x)] # prune ending zeros
y  = ifloat32(yn, data_type) # data type back normalization
wavfile.write('./output/'+filename+'_synth.wav', fs, y) # write WAV output file
```

# References
[1] A. A. Díaz Salazar, R. S. Mendes, "**Analysis/Synthesis Of The Andean Quena Via Harmonic Band Wavelet Transform**", In: Proceedings of the 18th International Conference on Digital Audio Effects (DAFx-15), 2015, pp. 1–4. [Online.](https://www.ntnu.edu/documents/1001201110/1266017954/DAFx-15_submission_74_v3.pdf).<br />
[2] A. A. Díaz Salazar, "HBWT_AnaSynth", Campinas, Brazil, 2015. <br />
[3] A. A. Díaz Salazar, “Analysis of musical instruments via the Harmonic Band Hurst Exponent: Comparative study of the Quena and other wind instruments” (in Portuguese), University of Campinas, 2015. [Online](http://repositorio.unicamp.br/handle/REPOSIP/259746).
[4] P. Polotti, G. Evangelista, "**Fractal Additive Synthesis via Harmonic-Band Wavelets**", In: Computer Music Journal, vol.25, no. 3, pp. 22–37, Mar. 2001.
