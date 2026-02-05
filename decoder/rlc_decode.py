def rlc_decode(pairs):
    ac = []
    for run, value in pairs:
        if run == 0 and value == 0:
            while len(ac) < 63:
                ac.append(0)
            break
        ac.extend([0] * run)
        ac.append(value)
    return ac
