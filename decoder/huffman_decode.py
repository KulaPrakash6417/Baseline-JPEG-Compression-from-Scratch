from encoder.huffman_tables import DC_LUMA_CODES, AC_LUMA_CODES


def invert_table(table):
    """
    Reverse Huffman table: bitstring -> symbol
    """
    return {v: k for k, v in table.items()}


# Inverted Huffman tables
DC_INV = invert_table(DC_LUMA_CODES)
AC_INV = invert_table(AC_LUMA_CODES)


def decode_symbol(reader, table):
    """
    Decode a Huffman symbol from the bitstream
    """
    code = ""
    while True:
        code += str(reader.read_bit())
        if code in table:
            return table[code]


def decode_dc(reader):
    """
    Decode one DC coefficient difference
    """
    # Huffman decode gives the SIZE (category)
    size = decode_symbol(reader, DC_INV)

    if size == 0:
        return 0

    # Read magnitude bits
    bits = reader.read_bits(size)

    # Convert to signed integer (JPEG rule)
    if bits < (1 << (size - 1)):
        bits -= (1 << size) - 1

    return bits


def decode_ac(reader):
    """
    Decode AC coefficients for ONE 8x8 block
    Returns a list of (run, value) pairs
    """
    pairs = []

    while True:
        symbol = decode_symbol(reader, AC_INV)

        # End Of Block (EOB)
        if symbol == 0x00:
            pairs.append((0, 0))
            break

        # Zero Run Length (ZRL): 16 zeros
        if symbol == 0xF0:
            pairs.append((15, 0))
            continue

        # Normal AC symbol
        run = symbol >> 4
        size = symbol & 0x0F

        bits = reader.read_bits(size)

        # Convert to signed
        if bits < (1 << (size - 1)):
            bits -= (1 << size) - 1

        pairs.append((run, bits))

    return pairs
