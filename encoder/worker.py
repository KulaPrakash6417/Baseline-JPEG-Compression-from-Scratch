from encoder.color import rgb_block_to_y
from encoder.dct import dct_2d
from encoder.quantization import quantize
from encoder.zigzag import zigzag_scan

_logged = False  # global flag

def process_block(rgb_block):
    global _logged

    Y = rgb_block_to_y(rgb_block)

    if not _logged:
        print("\n--- STAGE: RGB → Y (Luminance) ---")
        print("Before: RGB block shape:", rgb_block.shape)
        print("After: Y block shape:", Y.shape)
        print("Next: Apply DCT to convert spatial → frequency domain\n")
        _logged = True

    dct = dct_2d(Y)
    q = quantize(dct)
    zz = zigzag_scan(q)

    return zz[0], zz[1:]
