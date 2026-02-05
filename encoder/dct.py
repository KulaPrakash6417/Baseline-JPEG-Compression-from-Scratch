import numpy as np
import math

# Precompute the 8x8 DCT transform matrix
def create_dct_matrix():
    C = np.zeros((8, 8), dtype=np.float32)
    for u in range(8):
        for x in range(8):
            if u == 0:
                C[u, x] = 1 / math.sqrt(8)
            else:
                C[u, x] = math.sqrt(2/8) * math.cos((2*x + 1) * u * math.pi / 16)
    return C

# Global DCT matrix (computed once)
DCT_MATRIX = create_dct_matrix()
DCT_MATRIX_T = DCT_MATRIX.T


_logged_dct = False

def dct_2d(block):
    global _logged_dct
    if not _logged_dct:
        print("\n--- STAGE: Discrete Cosine Transform (DCT) ---")
        print("Before: 8x8 spatial pixel block")
        print("After: 8x8 frequency coefficients")
        print("Next: Quantization (lossy compression)\n")
        _logged_dct = True

    return DCT_MATRIX @ block @ DCT_MATRIX_T
