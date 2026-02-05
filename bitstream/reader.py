class BitReader:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.bit_pos = 0

    def read_bit(self):
        byte = self.data[self.pos]
        bit = (byte >> (7 - self.bit_pos)) & 1
        self.bit_pos += 1

        if self.bit_pos == 8:
            self.bit_pos = 0
            self.pos += 1
            if self.pos < len(self.data) and self.data[self.pos] == 0x00 and byte == 0xFF:
                self.pos += 1

        return bit

    def read_bits(self, n):
        val = 0
        for _ in range(n):
            val = (val << 1) | self.read_bit()
        return val
