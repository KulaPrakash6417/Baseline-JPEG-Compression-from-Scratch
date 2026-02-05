def rlc_encode(ac_coeffs):
    """
    Run-length encoding of 63 AC coefficients
    """
    result = []
    zero_count = 0

    for coeff in ac_coeffs:
        if coeff == 0:
            zero_count += 1
        else:
            result.append((zero_count, coeff))
            zero_count = 0

    # End Of Block
    result.append((0, 0))
    return result
