import numpy as np
import math

def pad_image_rgb(img):
    h, w, _ = img.shape
    H = math.ceil(h / 8) * 8
    W = math.ceil(w / 8) * 8

    padded = np.zeros((H, W, 3), dtype=img.dtype)
    padded[:h, :w] = img
    padded[h:, :w] = img[h-1:h, :, :]
    padded[:, w:] = padded[:, w-1:w, :]

    return padded

def rgb_blocks(img):
    h, w, _ = img.shape
    for i in range(0, h, 8):
        for j in range(0, w, 8):
            yield img[i:i+8, j:j+8]
