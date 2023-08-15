import numpy as np
import matplotlib.pyplot as plt

class advanced():
    def fouriersmooth(y,vac):
        rft = np.fft.rfft(y)
        rft[vac:] = 0   # Note, rft.shape = 21
        y_smooth = np.fft.irfft(rft)
        return y_smooth



