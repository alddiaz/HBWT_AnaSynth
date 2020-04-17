# Stereo to mono audio conversion
# Developed by Aldo Diaz
# University of Campinas, 2020

import numpy as np

# Monoaural signal conversion
def stereo2mono(x):
    # Input:
    # x: stereo audio signal
    #
    # Output:
    # x: mono audio signal (stereo channel average)

    y = x.sum(axis=1)/2.0 # mono audio conversion
    y = np.around(y)
    y = y.astype(x.dtype)

    return y
