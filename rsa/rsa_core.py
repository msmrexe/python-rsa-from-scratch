# rsa_core.py

"""
Core RSA logic for key generation, encryption, and decryption.

This module handles:
- Generating public/private key pairs.
- Encrypting string messages (with padding/blocking).
- Decrypting ciphertext (with padding/blocking).
"""

from .crypto_math import karatsuba_multiply, gcd, modinv, modexpo
from .utils import generate_prime_pair, bytes_to_int, int_to_bytes

# Standard public exponent
DEFAULT_E = 65537  # 2^16 + 1

def generate_keys(bits: int = 2048) -> tuple[tuple, tuple]:
    """
    Generates a new RSA public/private key pair.

    Args:
        bits (int): The total desired key size (e.g., 2048).
                    This will find two primes of bits/2.

    Returns:
        tuple[tuple, tuple]: A tuple containing:
                             (public_key, private_key)
                             where public_key is (e, n)
                             and private_key is (d, n).
    """
    prime_bits = bits // 2
    p, q = generate_prime_pair(bits=prime_bits)

    # Use Karatsuba multiply for n and phi
    n = karatsuba_multiply(p, q)
    phi = karatsuba_multiply(p - 1, q - 1)
    
    e = DEFAULT_E
    
    # Ensure e and phi are coprime
    while gcd(e, phi) != 1:
        # In the unlikely event 65537 is not coprime,
        # try another common one.
        e = 3  

    # Use Extended Euclidean Algorithm to find d
    d = modinv(e, phi)
    
    public_key = (e, n)
    private_key = (d, n)
    
    return public_key, private_key


def encrypt(message: str, public_key: tuple[int, int]) -> list[int]:
    """
    Encrypts a string message using a public key.

    The message is encoded to bytes, split into appropriate-sized
    blocks, and each block is encrypted.

    Args:
        message (str): The plaintext message to encrypt.
        public_key (tuple[int, int]): The public key (e, n).

    Returns:
        list[int]: A list of integers representing the encrypted blocks.
    """
    e, n = public_key
    
    # Calculate max block size in bytes
    # -1 to ensure message int is always < n
    key_bytes = (n.bit_length() + 7) // 8
    max_block_size = key_bytes - 1  
    
    if max_block_size <= 0:
        raise ValueError("Key size is too small to encrypt any data.")

    encrypted_blocks = []
    # Encode string to bytes (crucial step)
    message_bytes = message.encode('utf-8')
    
    # Split message into blocks
    for i in range(0, len(message_bytes), max_block_size):
        block = message_bytes[i:i + max_block_size]
        
        # Convert byte block to integer
        m = bytes_to_int(block)
        
        # Encrypt: c = m^e mod n
        c = modexpo(m, e, n)
        encrypted_blocks.append(c)
        
    return encrypted_blocks


def decrypt(cipher_blocks: list[int], private_key: tuple[int, int]) -> str:
    """
    Decrypts a list of encrypted blocks into a string.

    Args:
        cipher_blocks (list[int]): List of encrypted integers.
        private_key (tuple[int, int]): The private key (d, n).

    Returns:
        str: The decrypted plaintext message.
    """
    d, n = private_key
    
    decrypted_bytes = b''
    
    for c in cipher_blocks:
        # Decrypt: m = c^d mod n
        m = modexpo(c, d, n)
        
        # Convert decrypted integer back to bytes
        block_bytes = int_to_bytes(m)

        decrypted_bytes += block_bytes
        
    # Decode from bytes back to string, ignoring errors
    return decrypted_bytes.decode('utf-8', errors='ignore')
