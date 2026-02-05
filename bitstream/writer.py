class BitWriter:
    def __init__(self):
        self.buffer = bytearray()
        self.current_byte = 0
        self.bit_count = 0

    def write_bits(self, bits):
        """
        bits: string of '0' and '1'
        """
        for bit in bits:
            self.current_byte = (self.current_byte << 1) | (bit == '1')
            self.bit_count += 1

            if self.bit_count == 8:
                self.buffer.append(self.current_byte)
                # Byte stuffing
                if self.current_byte == 0xFF:
                    self.buffer.append(0x00)
                self.current_byte = 0
                self.bit_count = 0

    def flush(self):
    # Flush remaining bits and force byte alignment as required by JPEG
        if self.bit_count > 0:
            self.current_byte <<= (8 - self.bit_count)
            self.buffer.append(self.current_byte)
            if self.current_byte == 0xFF:
                self.buffer.append(0x00)
            self.current_byte = 0
            self.bit_count = 0


    def get_bytes(self):
        return bytes(self.buffer)
