from encoder.huffman_tables import DC_LUMA_CODES, AC_LUMA_CODES

def invert_table(table):
    return {v: k for k, v in table.items()}

DC_INV = invert_table(DC_LUMA_CODES)
AC_INV = invert_table(AC_LUMA_CODES)

def decode_symbol(reader, table):
    code = ""
    while True:
        code += str(reader.read_bit())
        if code in table:
            return table[code]
