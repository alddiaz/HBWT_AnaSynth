# Stereo to mono audio conversion
# Developed by Aldo Diaz
# University of Campinas, 2020

# Monoaural signal conversion
def stereo2mono(x):
    # Input:
    # x: stereo audio signal
    #
    # Output:
    # x: mono audio signal (stereo channel average)

    y = x.sum(axis=1)/2 # mono audio conversion

    return y
