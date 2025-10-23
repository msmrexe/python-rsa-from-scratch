# utils.py

"""
Utility functions for the RSA implementation, primarily for
prime number generation.
"""

import time
from .crypto_math import lcg_prng, is_prime

def generate_prime_pair(bits: int = 1024) -> tuple[int, int]:
    """
    Generates two distinct large prime numbers, p and q.

    Uses the LCG pseudo-random number generator and the
    Miller-Rabin primality test.

    Args:
        bits (int): The target bit length for the primes (e.g., 1024).

    Returns:
        tuple[int, int]: (p, q), two distinct primes.
    """
    print(f"Searching for {bits}-bit prime 'p'...")
    # Seed the LCG with the current time
    generator = lcg_prng(time.time(), bits=bits)
    
    while True:
        p = next(generator)
        if is_prime(p, 20):
            print(f"Found prime p: {str(p)[:20]}...")
            break
            
    print(f"Searching for {bits}-bit prime 'q'...")
    while True:
        q = next(generator)
        if p != q and is_prime(q, 20):
            print(f"Found prime q: {str(q)[:20]}...")
            break
            
    return p, q


def bytes_to_int(byte_block: bytes) -> int:
    """
    Converts a block of bytes into a large integer.
    
    This function implements the logic of your original 'blockOrd'
    but operates on bytes for robustness. It treats the byte
    block as a base-256 number in little-endian order.
    
    Args:
        byte_block (bytes): The block of bytes to convert.
    
    Returns:
        int: The resulting large integer.
    """
    integer = 0
    for i, byte in enumerate(byte_block):
        # (256 ** i) is the same as (1 << (8 * i))
        integer += byte * (256 ** i)
    return integer


def int_to_bytes(integer: int) -> bytes:
    """
    Converts a large integer back into a block of bytes.
    
    This function implements the logic of your original 'blockChr'
    but operates on bytes. It's the exact inverse of
    bytes_to_int.
    
    Args:
        integer (int): The large integer to convert.
    
    Returns:
        bytes: The resulting block of bytes.
    """
    byte_list = []
    temp_int = integer
    
    if temp_int == 0:
        return b'\x00'
        
    while temp_int > 0:
        # Get the least significant byte
        byte_code = temp_int % 256
        byte_list.append(byte_code)
        # Shift down by one byte
        temp_int //= 256
    
    return bytes(byte_list)
