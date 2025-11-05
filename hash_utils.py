"""
Custom hash function for blockchain.
"""

MASK64 = (1 << 64) - 1


def _rotate_left(x, r):
    """Rotate left with 64-bit boundary."""
    r &= 63
    return ((x << r) & MASK64) | (x >> (64 - r))


def my_hash(data: str) -> str:
    """
    Hash function that generates a 64-character hexadecimal hash (256 bits).
    Args:data: Input string to hash
    Returns: 64-character hexadecimal hash string
    """
    # Initialize four 64-bit states
    a = 0x1A2B3C4D5E6F7788
    b = 0x8899AABBCCDDEEFF
    c = 0x0123456789ABCDEF
    d = 0xF0E1D2C3B4A59687

    # Convert to bytes
    bytes_data = data.encode("utf-8")

    # Process each byte
    for ch in bytes_data:
        a ^= ch
        a = _rotate_left(a, 7)
        a = (a * 33 + (ch ^ (ch >> 2))) & MASK64

        b ^= _rotate_left(ch, 11)
        b = (b * 29 + (ch ^ (ch >> 4))) & MASK64

        c ^= _rotate_left(ch, 19)
        c = (c * 35 + (ch ^ (ch >> 6))) & MASK64

        d ^= _rotate_left(ch, 23)
        d = (d * 39 + (ch ^ (ch >> 8))) & MASK64

    # Final mixing
    a ^= _rotate_left(b, 13)
    a = (a + c) & MASK64
    
    b ^= _rotate_left(c, 17)
    b = (b + d) & MASK64
    
    c ^= _rotate_left(d, 29)
    c = (c + a) & MASK64
    
    d ^= _rotate_left(a, 31)
    d = (d + b) & MASK64

    # Combine four 64-bit states into 256-bit hash (64 hex characters)
    return f"{a:016x}{b:016x}{c:016x}{d:016x}"