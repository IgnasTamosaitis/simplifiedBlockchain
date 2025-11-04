def my_hash(data: str) -> str:
    """
    Custom hash function that generates a 64-character hexadecimal hash.
    
    Args:
        data: Input string to hash
        
    Returns:
        64-character hexadecimal hash string
    """
    # Simple custom hash algorithm
    # Note: This is for educational purposes only, not cryptographically secure
    
    hash_value = 0
    prime = 31
    mod = 2**256  # To simulate 256-bit hash
    
    for i, char in enumerate(data):
        hash_value = (hash_value * prime + ord(char) * (i + 1)) % mod
    
    # Convert to 64-character hex string
    hex_hash = format(hash_value, '064x')
    
    return hex_hash