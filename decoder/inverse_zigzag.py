import numpy as np
from encoder.zigzag import ZIGZAG_ORDER

def inverse_zigzag(arr):
    block = np.zeros((8,8), dtype=np.float32)
    for idx, (i, j) in enumerate(ZIGZAG_ORDER):
        block[i, j] = arr[idx]
    return block
