import numpy as np
from bitstream.reader import BitReader
from decoder.huffman_decode import decode_symbol, DC_INV, AC_INV
from decoder.dpcm_decode import dpcm_decode
from decoder.rlc_decode import rlc_decode
from decoder.inverse_zigzag import inverse_zigzag
from decoder.dequantization import dequantize
from decoder.idct import idct_2d

def decode_entropy(entropy_data, num_blocks):
    reader = BitReader(entropy_data)
    dc_diffs = []
    ac_blocks = []

    for _ in range(num_blocks):
        cat = decode_symbol(reader, DC_INV)
        diff = reader.read_bits(cat) if cat > 0 else 0
        dc_diffs.append(diff)

        ac_pairs = []
        while True:
            sym = decode_symbol(reader, AC_INV)
            if sym == (0,0):
                ac_pairs.append((0,0))
                break
            run = sym >> 4
            size = sym & 0x0F
            val = reader.read_bits(size)
            ac_pairs.append((run, val))
        ac_blocks.append(ac_pairs)

    return dc_diffs, ac_blocks

def reconstruct_image(dc_diffs, ac_blocks, height, width):
    dc_vals = dpcm_decode(dc_diffs)
    blocks = []

    for dc, ac in zip(dc_vals, ac_blocks):
        coeffs = [dc] + rlc_decode(ac)
        block = inverse_zigzag(coeffs)
        block = dequantize(block)
        block = idct_2d(block)
        blocks.append(block)

    img = np.zeros((height, width))
    idx = 0
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            img[i:i+8, j:j+8] = blocks[idx]
            idx += 1

    img += 128
    return np.clip(img, 0, 255).astype(np.uint8)
