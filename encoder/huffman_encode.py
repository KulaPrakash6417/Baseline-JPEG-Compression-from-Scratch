from encoder.huffman_tables import DC_LUMA_CODES, AC_LUMA_CODES

def magnitude_category(value):
    """
    Compute JPEG magnitude category and bit representation
    """
    value = int(value)

    if value == 0:
        return 0, ""

    abs_val = abs(value)
    category = abs_val.bit_length()
    bits = format(abs_val, f'0{category}b')

    if value < 0:
        bits = ''.join('1' if b == '0' else '0' for b in bits)

    return category, bits



_logged_entropy = False

def encode_dc(diff):
    global _logged_entropy
    if not _logged_entropy:
        print("\n--- STAGE: Entropy Coding ---")
        print("DC: DPCM + Huffman coding")
        print("AC: Run-Length + Huffman coding")
        print("Next: Bitstream written into JPEG format\n")
        _logged_entropy = True

    category, bits = magnitude_category(diff)
    return DC_LUMA_CODES[category] + bits



def encode_ac(rlc_pairs):
    """
    Encode AC coefficients using canonical JPEG Huffman coding
    """
    bitstream = ""

    for run, value in rlc_pairs:
        # End Of Block
        if run == 0 and value == 0:
            symbol = 0x00  # EOB
            bitstream += AC_LUMA_CODES[symbol]
            break

        value = int(value)
        category, bits = magnitude_category(value)

        # Handle long zero runs using ZRL
        while run >= 16:
            symbol = 0xF0  # ZRL (15,0)
            bitstream += AC_LUMA_CODES[symbol]
            run -= 16

        # Normal AC symbol
        symbol = (run << 4) | category
        bitstream += AC_LUMA_CODES[symbol]
        bitstream += bits

    return bitstream


