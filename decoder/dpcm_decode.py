def dpcm_decode(diffs):
    values = []
    prev = 0
    for d in diffs:
        val = prev + d
        values.append(val)
        prev = val
    return values
