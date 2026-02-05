def dpcm_encode(dc_coeffs):
    """
    Differential encoding of DC coefficients
    """
    diffs = []
    prev = 0
    for dc in dc_coeffs:
        diff = dc - prev
        diffs.append(diff)
        prev = dc
    return diffs
