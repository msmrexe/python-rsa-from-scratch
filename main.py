# main.py

"""
RSA Encryption System - Command-Line Interface

This script provides a CLI for the RSA project, allowing users to:
1. Generate new public/private key pairs.
2. Encrypt a message using a public key.
3. Decrypt a message using a private key.

This script is the main entry point for the application.
"""

import argparse
import rsa_core

def save_key_to_file(key: tuple, filename: str):
    """Saves a key (e, n) or (d, n) to a file."""
    with open(filename, 'w') as f:
        f.write(f"{key[0]}\n")  # e or d
        f.write(f"{key[1]}\n")  # n
    print(f"Saved key to {filename}")

def read_key_from_file(filename: str) -> tuple[int, int]:
    """Reads a key (e, n) or (d, n) from a file."""
    with open(filename, 'r') as f:
        part1 = int(f.readline().strip())
        part2 = int(f.readline().strip())
    return (part1, part2)

def save_cipher_to_file(blocks: list[int], filename: str):
    """Saves encrypted blocks to a file, one per line."""
    with open(filename, 'w') as f:
        for block in blocks:
            f.write(f"{block}\n")
    print(f"Saved ciphertext to {filename}")

def read_cipher_from_file(filename: str) -> list[int]:
    """Reads encrypted blocks from a file."""
    blocks = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                blocks.append(int(line.strip()))
    return blocks

def main():
    """Parses command-line arguments and executes the requested command."""
    parser = argparse.ArgumentParser(
        description="RSA Encryption System - (Advanced Programming Final Project)",
        epilog="Example: python main.py generate -b 2048"
    )
    
    subparsers = parser.add_subparsers(dest='command', required=True,
                                       help="Sub-command to run")

    # --- Generate Keys Command ---
    gen_parser = subparsers.add_parser(
        'generate', 
        help="Generate a new public/private key pair."
    )
    gen_parser.add_argument(
        '-b', '--bits', 
        type=int, 
        default=2048,
        help="Key size in bits (default: 2048). Must be an even number."
    )
    gen_parser.add_argument(
        '--pub', 
        default='public.key',
        help="Output file for the public key (default: public.key)"
    )
    gen_parser.add_argument(
        '--priv',
        default='private.key',
        help="Output file for the private key (default: private.key)"
    )

    # --- Encrypt Command ---
    enc_parser = subparsers.add_parser(
        'encrypt',
        help="Encrypt a message using a public key."
    )
    enc_parser.add_argument(
        '-m', '--message',
        type=str,
        required=True,
        help="The plaintext message to encrypt (as a string)."
    )
    enc_parser.add_argument(
        '-k', '--key',
        type=str,
        default='public.key',
        help="Path to the public key file (default: public.key)"
    )
    enc_parser.add_argument(
        '-o', '--out',
        default='ciphertext.txt',
        help="Output file for the ciphertext (default: ciphertext.txt)"
    )

    # --- Decrypt Command ---
    dec_parser = subparsers.add_parser(
        'decrypt',
        help="Decrypt a message using a private key."
    )
    dec_parser.add_argument(
        '-c', '--cipher',
        type=str,
        default='ciphertext.txt',
        help="Path to the ciphertext file (default: ciphertext.txt)"
    )
    dec_parser.add_argument(
        '-k', '--key',
        type=str,
        default='private.key',
        help="Path to the private key file (default: private.key)"
    )

    args = parser.parse_args()

    # --- Execute Command Logic ---
    if args.command == 'generate':
        print(f"Generating {args.bits}-bit key pair... This may take a moment.")
        if args.bits % 2 != 0:
            print("Error: Key bits must be an even number.")
            return
            
        pub_key, priv_key = rsa_core.generate_keys(bits=args.bits)
        save_key_to_file(pub_key, args.pub)
        save_key_to_file(priv_key, args.priv)
        print("Key generation complete.")
        
    elif args.command == 'encrypt':
        print(f"Encrypting message using key from {args.key}...")
        try:
            pub_key = read_key_from_file(args.key)
            encrypted_blocks = rsa_core.encrypt(args.message, pub_key)
            save_cipher_to_file(encrypted_blocks, args.out)
            print("Encryption complete.")
        except FileNotFoundError:
            print(f"Error: Key file not found at {args.key}")
        except Exception as e:
            print(f"An error occurred during encryption: {e}")

    elif args.command == 'decrypt':
        print(f"Decrypting ciphertext from {args.cipher} using key {args.key}...")
        try:
            priv_key = read_key_from_file(args.key)
            cipher_blocks = read_cipher_from_file(args.cipher)
            decrypted_message = rsa_core.decrypt(cipher_blocks, priv_key)
            print("\n--- Decrypted Message ---")
            print(decrypted_message)
            print("-------------------------")
        except FileNotFoundError:
            print(f"Error: File not found. Check paths for {args.cipher} and {args.key}")
        except Exception as e:
            print(f"An error occurred during decryption: {e}")

if __name__ == '__main__':
    main()
