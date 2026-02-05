import numpy as np

def rgb_block_to_y(block):
    """
    Convert an 8x8 RGB block to Y (luminance), level-shifted
    """
    block = block.astype(np.float32)

    R = block[:, :, 0]
    G = block[:, :, 1]
    B = block[:, :, 2]

    Y = 0.299 * R + 0.587 * G + 0.114 * B
    return Y - 128.0
