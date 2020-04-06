# Data type 'float32' normalization library
# Developed by Aldo Diaz
# University of Campinas, 2020

import numpy as np

# Data type normalization to 'float32' range [-1.0, 1.0]
def float32(x):
    data_type = str(x.dtype)

    if data_type != 'uint8':
        if data_type != 'float32':
            bit_res = [digit for digit in data_type if digit.isdigit()]
            bits = int(''.join(map(str, bit_res)))
            x = ((x+pow(2, bits-1))/float(pow(2, bits)-1)-0.5)*2.0
    else:
        x = ((x/float(pow(2, 8)-1))-0.5)*2.0

    return x, data_type

# Data type back normalization
def ifloat32(x, data_type):
    if data_type != 'uint8':
        if data_type != 'float32':
            bit_res = [digit for digit in data_type if digit.isdigit()]
            bits = int(''.join(map(str, bit_res)))
            x = (x/2.0+0.5)*float(pow(2, bits)-1)-pow(2, bits-1)
            x = np.around(x)
            x = x.astype(data_type)
    else:
        x = (x/2.0+0.5)*float(pow(2, 8)-1)
        x = np.around(x)
        x = x.astype('uint8')

    return x
