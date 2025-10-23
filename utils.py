# utils.py

"""
Utility functions for the RSA implementation, primarily for
prime number generation.
"""

import time
from crypto_math import lcg_prng, is_prime

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
