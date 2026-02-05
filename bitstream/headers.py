import struct
from bitstream.markers import *
from encoder.huffman_tables import (
    DC_LUMA_BITS, DC_LUMA_VALS,
    AC_LUMA_BITS, AC_LUMA_VALS
)

def write_app0():
    return (
        APP0 +
        struct.pack(">H", 16) +
        b"JFIF\x00" +
        b"\x01\x01" +
        b"\x00" +
        b"\x00\x01\x00\x01" +
        b"\x00\x00"
    )

def write_dqt(qtable):
    data = b'\x00' + qtable.flatten().astype('uint8').tobytes()
    return DQT + struct.pack(">H", len(data) + 2) + data

def write_sof0(height, width):
    """
    Baseline DCT Frame Header (SOF0)
    Single component (Y only)
    """
    return (
        SOF0 +
        struct.pack(">H", 11) +      # ✔ correct length for 1 component
        b"\x08" +                    # Sample precision = 8 bits
        struct.pack(">H", height) +
        struct.pack(">H", width) +
        b"\x01" +                    # Number of components = 1
        b"\x01" +                    # Component ID = 1 (Y)
        b"\x11" +                    # Sampling factors (1x1)
        b"\x00"                      # Quant table ID = 0
    )


def write_dht():
    """
    Write JPEG Define Huffman Table (DHT) segment
    for luminance DC and AC tables.
    """

    data = bytearray()

    # ---- DC Luminance Table (class=0, id=0) ----
    data.append(0x00)  # HT info: DC, table 0
    data.extend(DC_LUMA_BITS)
    data.extend(DC_LUMA_VALS)

    # ---- AC Luminance Table (class=1, id=0) ----
    data.append(0x10)  # HT info: AC, table 0
    data.extend(AC_LUMA_BITS)
    data.extend(AC_LUMA_VALS)

    # Length includes the 2 bytes of length field itself
    length = len(data) + 2

    return DHT + struct.pack(">H", length) + data

def write_sos():
    return (
        SOS +
        struct.pack(">H", 8) +
        b"\x01" +
        b"\x01\x00" +
        b"\x00\x3F\x00"
    )
