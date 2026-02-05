from encoder.quantization import Q_LUMA

def dequantize(block):
    return block * Q_LUMA
