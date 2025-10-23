# RSA Encryption System

This project is a Python-based implementation of the RSA (Rivest–Shamir–Adleman) cryptosystem. It was developed as a final project for an advanced Python programming course, demonstrating the core algorithms behind asymmetric encryption from scratch.

The system can generate public/private key pairs, encrypt plaintext messages, and decrypt ciphertext.

## Features

* **Key Generation**: Creates RSA key pairs of arbitrary bit length (e.g., 2048, 4096).
* **Encryption**: Encrypts string messages into a series of ciphertext numbers.
* **Decryption**: Decrypts ciphertext numbers back into the original string.
* **Custom Math Implementation**: Implements all core algorithms to show a foundational understanding, including:
    * **Miller-Rabin Primality Test** for finding large primes.
    * **Linear Congruential Generator (LCG)** as a simple PRNG to find prime candidates (for academic purposes).
    * **Karatsuba Algorithm** for fast multiplication of large integers.
    * **Extended Euclidean Algorithm** for finding the modular multiplicative inverse (`d`).
* **Secure Primitives**: Uses Python's `secrets` module for cryptographically secure random number generation during primality testing.
* **Robust Blocking**: Automatically handles message blocking and padding based on key size.
* **CLI Interface**: A clean, command-line interface using `argparse` for all operations.

## Project Structure

The project is organized into a modular structure for clarity and maintainability:

```
python-rsa-from-scratch/
├── .gitignore            # Git ignore file
├── LICENSE               # MIT license file
├── README.md             # This documentation file
├── main.py               # Main runnable script with the argparse CLI
└── rsa/
    ├── __init__.py      # Initialize package
    ├── crypto_math.py   # Core math: Miller-Rabin, Karatsuba, EGCD, etc.
    ├── rsa_core.py      # High-level RSA logic: generate_keys, encrypt, decrypt
    └── utils.py         # Helper functions (e.g., prime pair generation)
```

## Usage

This project is a command-line application.

### 1. Generate Keys

First, generate your public and private keys. You can specify the bit size (default is 2048).

```bash
# Generate a standard 2048-bit key pair
python main.py generate

# Generate a stronger 4096-bit key pair
python main.py generate --bits 4096

# Specify custom output filenames
python main.py generate -b 2048 --pub my_public.key --priv my_private.key
```

This will create two files (e.g., `public.key` and `private.key`) in your directory.

### 2. Encrypt a Message

Use the `encrypt` command with your public key to encrypt a message.

```bash
# Encrypt a message using the default public.key
python main.py encrypt -m "Hello, this is a secret message!"

# Specify the key file and output file
python main.py encrypt -m "My secret" -k my_public.key -o secret.txt
```

This will create a ciphertext file (e.g., `ciphertext.txt`).

### 3. Decrypt a Message

Use the `decrypt` command with your private key to read the ciphertext and reveal the original message.

```bash
# Decrypt the default ciphertext.txt using the default private.key
python main.py decrypt

# Specify the ciphertext and private key files
python main.py decrypt -c secret.txt -k my_private.key
```

The decrypted message will be printed directly to your console.

```
$ python main.py decrypt
Decrypting ciphertext from ciphertext.txt using key private.key...

--- Decrypted Message ---
Hello, this is a secret message!
-------------------------
```

---

## Author

Feel free to connect or reach out if you have any questions!

* **Maryam Rezaee**
* **GitHub:** [@msmrexe](https://github.com/msmrexe)
* **Email:** [ms.maryamrezaee@gmail.com](mailto:ms.maryamrezaee@gmail.com)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.
