import numpy as np
import math

def mse(original, reconstructed):
    return np.mean((original - reconstructed) ** 2)

def psnr(original, reconstructed):
    return 20 * math.log10(255 / math.sqrt(mse(original, reconstructed)))
