import numpy as np
from bitstream.reader import BitReader
from decoder.huffman_decode import decode_symbol, DC_INV, AC_INV
from decoder.dpcm_decode import dpcm_decode
from decoder.rlc_decode import rlc_decode
from decoder.inverse_zigzag import inverse_zigzag
from decoder.dequantization import dequantize
from decoder.idct import idct_2d
from encoder.zigzag import ZIGZAG_ORDER
from encoder.quantization import Q_LUMA
from encoder.dct import DCT_MATRIX, DCT_MATRIX_T
from decoder.huffman_decode import decode_dc, decode_ac


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



def inverse_zigzag(coeffs):
    block = np.zeros((8, 8))
    for idx, (i, j) in enumerate(ZIGZAG_ORDER):
        block[i, j] = coeffs[idx]
    return block


def dequantize(block):
    return block * Q_LUMA


def idct_2d(block):
    return (DCT_MATRIX_T @ block @ DCT_MATRIX).astype(np.float32)


def decode_jpeg(jpeg_path):
    """
    Decode JPEG produced by our encoder
    Returns reconstructed grayscale image
    """
    with open(jpeg_path, "rb") as f:
        data = f.read()

    # --------------------------------------------------
    # 1. Parse SOF0 (image size)
    # --------------------------------------------------
    sof = data.find(b'\xFF\xC0')
    if sof == -1:
        raise ValueError("SOF0 not found")

    height = int.from_bytes(data[sof + 5: sof + 7], "big")
    width  = int.from_bytes(data[sof + 7: sof + 9], "big")

    blocks_x = width // 8
    blocks_y = height // 8
    total_blocks = blocks_x * blocks_y

    # --------------------------------------------------
    # 2. Locate entropy-coded data
    # --------------------------------------------------
    sos = data.find(b'\xFF\xDA')
    if sos == -1:
        raise ValueError("SOS not found")

    sos_len = int.from_bytes(data[sos + 2: sos + 4], "big")
    entropy_start = sos + 2 + sos_len

    eoi = data.find(b'\xFF\xD9')
    entropy_data = data[entropy_start:eoi]

    # --------------------------------------------------
    # 3. Huffman decoding
    # --------------------------------------------------
    reader = BitReader(entropy_data)

    dc_diffs = []
    ac_blocks = []

    for _ in range(total_blocks):
        dc = decode_dc(reader)
        ac = decode_ac(reader)
        dc_diffs.append(dc)
        ac_blocks.append(ac)

    # --------------------------------------------------
    # 4. DC DPCM decoding
    # --------------------------------------------------
    dc_coeffs = dpcm_decode(dc_diffs)

    # --------------------------------------------------
    # 5. Reconstruct image
    # --------------------------------------------------
    image = np.zeros((height, width), dtype=np.uint8)

    idx = 0
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            coeffs = [dc_coeffs[idx]] + rlc_decode(ac_blocks[idx])

            block = inverse_zigzag(coeffs)
            block = dequantize(block)
            block = idct_2d(block)

            block = block + 128
            block = np.clip(block, 0, 255).astype(np.uint8)

            image[y:y+8, x:x+8] = block
            idx += 1


    return np.clip(image, 0, 255).astype(np.uint8)
