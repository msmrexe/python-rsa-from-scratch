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

## How It Works

The RSA algorithm's security relies on the practical difficulty of factoring the product of two large prime numbers (factoring `n` into `p` and `q`). The process is split into three phases:

### 1\. Key Generation

This is the most complex step, where the public and private keys are created.

1.  **Find Primes**: Two distinct, large prime numbers, $p$ and $q$, are found.
      * This implementation uses the **LCG** (`lcg_prng`) to generate large random number candidates.
      * Each candidate is checked for primality using the **Miller-Rabin Primality Test** (`is_prime`).
2.  **Calculate Modulus**: The modulus $n$ is calculated by multiplying the primes:
      * $n = p \times q$
      * This implementation uses the **Karatsuba Algorithm** (`karatsuba_multiply`) for this large multiplication.
      * $n$ is used for *both* the public and private keys.
3.  **Calculate Totient**: Euler's totient function, $\phi(n)$, is calculated.
      * $\phi(n) = (p-1) \times (q-1)$
      * This value is kept secret and is crucial for finding the private key.
4.  **Find Public Exponent ($e$)**: An integer $e$ is chosen such that $1 < e < \phi(n)$ and $e$ is coprime to $\phi(n)$ (i.e., $\text{gcd}(e, \phi(n)) = 1$).
      * This implementation uses the common standard $e = 65537$ ($2^{16} + 1$).
5.  **Find Private Exponent ($d$)**: The private exponent $d$ is calculated as the modular multiplicative inverse of $e$ modulo $\phi(n)$.
      * $d \equiv e^{-1} \pmod{\phi(n)}$
      * This implementation finds $d$ using the **Extended Euclidean Algorithm** (`egcd` and `modinv`).

**The Keys:**

  * **Public Key**: $(e, n)$. This pair is shared publicly for encrypting messages.
  * **Private Key**: $(d, n)$. This pair is kept secret for decrypting messages.

### 2\. Message Blocking

Before encryption, the string message (e.g., "Hello") must be converted into one or more integers ($m$) that are smaller than $n$.

1.  The string is encoded into `bytes` (e.g., UTF-8).
2.  These bytes are split into blocks, each small enough to ensure the resulting integer $m$ is less than $n$.
3.  Each block of bytes is converted into a large integer using the `bytes_to_int` function (which treats the bytes as a base-256 number).

### 3\. Encryption

With the public key $(e, n)$ and a message block $m$, the ciphertext $c$ is calculated:
$$c = m^e \pmod{n}$$

  * This is performed by the `modexpo` function (modular exponentiation).

### 4\. Decryption

With the private key $(d, n)$ and a ciphertext block $c$, the original message block $m$ is recovered:
$$m = c^d \pmod{n}$$

  * This also uses the efficient `modexpo` function. The recovered integer $m$ is then converted back into bytes using `int_to_bytes` and decoded into a string.

## Project Structure

This project is structured as a Python package for clean separation of concerns:

```
python-rsa-from-scratch/
├── .gitignore            # Git ignore file
├── LICENSE               # MIT license file
├── README.md             # This documentation file
├── main.py               # Main runnable script with the argparse CLI
└── rsa/
    ├── __init__.py       # Initialize package
    ├── crypto_math.py    # Core math: Miller-Rabin, Karatsuba, EGCD, etc.
    ├── rsa_core.py       # High-level RSA logic: generate_keys, encrypt, decrypt
    └── utils.py          # Helper functions (e.g., prime pair generation)
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
