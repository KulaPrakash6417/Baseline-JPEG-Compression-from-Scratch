import numpy as np
import math

def idct_2d(block):
    out = np.zeros((8,8), dtype=np.float32)

    for x in range(8):
        for y in range(8):
            s = 0.0
            for u in range(8):
                for v in range(8):
                    cu = 1/math.sqrt(2) if u==0 else 1
                    cv = 1/math.sqrt(2) if v==0 else 1
                    s += cu * cv * block[u,v] * \
                         math.cos((2*x+1)*u*math.pi/16) * \
                         math.cos((2*y+1)*v*math.pi/16)
            out[x,y] = 0.25 * s

    return out
