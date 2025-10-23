# crypto_math.py

"""
Core cryptographic math functions for the RSA implementation.

This module contains the low-level building blocks, including:
- Miller-Rabin primality test
- Modular exponentiation
- Karatsuba fast multiplication
- Extended Euclidean algorithm for modular inverse

This code is intended for academic purposes to demonstrate the
underlying algorithms of RSA.
"""

import sys
import secrets  # Use secrets for cryptographically strong random numbers

# Set higher recursion depth for deep recursive calls
# in egcd and karatsuba_multiply
try:
    sys.setrecursionlimit(2**20)
except (OverflowError, ValueError):
    print("Warning: Could not set high recursion depth.")


def lcg_prng(seed: int, bits: int = 1024):
    """
    Yields pseudo-random numbers using a Linear Congruential Generator (LCG).

    The parameters are chosen to generate large numbers suitable for
    finding primes of a specific bit length.

    Args:
        seed (int): The initial seed, often derived from system time.
        bits (int): The target bit length for the random numbers.
                    Primes will be around this length.

    Yields:
        int: A new pseudo-random number.
    """
    m = 2**bits
    a = 2**(bits // 2)
    c = 1  # A non-zero constant
    
    current_seed = int(seed)
    while True:
        current_seed = (a * current_seed + c) % m
        yield current_seed


def is_prime(n: int, k: int = 20) -> bool:
    """
    Checks if a number is prime using the Miller-Rabin primality test.

    Args:
        n (int): The number to test.
        k (int): The number of rounds to perform (accuracy).

    Returns:
        bool: True if n is probably prime, False if it is composite.
    """
    # Handle corner cases
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Find d such that n - 1 = 2^r * d
    d = n - 1
    while d % 2 == 0:
        d //= 2

    # Witness loop (repeat k times for accuracy)
    for _ in range(k):
        if not _miller_rabin_test(d, n):
            return False  # n is composite
    
    return True  # n is probably prime


def _miller_rabin_test(d: int, n: int) -> bool:
    """
    Performs a single round of the Miller-Rabin test.

    Args:
        d (int): Odd number such that n-1 = 2^r * d.
        n (int): The number to test.

    Returns:
        bool: True if the test passes (n might be prime), 
              False if the test fails (n is composite).
    """
    # Pick a random number 'a' in range [2, n-2]
    # Use secrets module for cryptographic security
    a = secrets.randbelow(n - 3) + 2  # Generates a in [2, n-2]

    # Calculate x = (a^d) % n
    x = modexpo(a, d, n)

    if x == 1 or x == n - 1:
        return True  # Test passes

    # Keep squaring x while d != n-1
    while d != n - 1:
        x = (x * x) % n
        d *= 2

        if x == 1:
            return False  # n is composite
        if x == n - 1:
            return True   # Test passes

    return False  # n is composite


def modexpo(x: int, y: int, d: int) -> int:
    """
    Calculates modular exponentiation (x^y) % d efficiently.

    Args:
        x (int): The base.
        y (int): The exponent.
        d (int): The modulus.

    Returns:
        int: The result of (x^y) % d.
    """
    result = 1
    x = x % d  # Reduce x modulo d
    
    while y > 0:
        # If y is odd, multiply x with result
        if y & 1:
            result = (result * x) % d
        
        # y must be even now
        y = y >> 1  # y = y / 2
        x = (x * x) % d  # x = x^2 % d
    
    return result


def power(x: int, y: int) -> int:
    """
    Calculates (x^y) using fast multiplication.
    For positive inputs only.

    Args:
        x (int): The base.
        y (int): The exponent.

    Returns:
        int: The result of x^y.
    """
    if y == 0:
        return 1
    if y == 1:
        return x
    
    n = x
    for _ in range(2, y + 1):
        x = karatsuba_multiply(x, n)
    return x


def karatsuba_multiply(x: int, y: int) -> int:
    """
    Multiplies two large integers using the Karatsuba algorithm.

    Args:
        x (int): The first number.
        y (int): The second number.

    Returns:
        int: The product x * y.
    """
    # Base case for recursion
    if x < 10 or y < 10:
        return x * y

    # Calculate the size of the numbers
    s = max(len(str(x)), len(str(y)))
    m = s // 2

    # Split the numbers into two halves
    a = x // (10**m)
    b = x % (10**m)
    c = y // (10**m)
    d = y % (10**m)

    # Recursive calls
    z0 = karatsuba_multiply(b, d)
    z1 = karatsuba_multiply((a + b), (c + d))
    z2 = karatsuba_multiply(a, c)

    # Combine the results
    return (z2 * 10**(2 * m)) + ((z1 - z2 - z0) * 10**m) + z0


def egcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    Finds gcd(a, b) and coefficients x, y such that ax + by = gcd(a, b).

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        tuple[int, int, int]: (gcd, x, y)
    """
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = egcd(b % a, a)
    
    # Update x and y using results of recursive call
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y


def modinv(e: int, phi: int) -> int:
    """
    Finds the modular multiplicative inverse of e modulo phi.

    Args:
        e (int): The number to find the inverse of.
        phi (int): The modulus.

    Returns:
        int: The modular inverse d, such that (e * d) % phi = 1.
    """
    g, x, y = egcd(e, phi)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    
    return x % phi


def gcd(e: int, phi: int) -> int:
    """
    Calculates the Greatest Common Divisor of two numbers.

    Args:
        e (int): First number.
        phi (int): Second number.

    Returns:
        int: The gcd(e, phi).
    """
    g, _, _ = egcd(e, phi)
    return g
