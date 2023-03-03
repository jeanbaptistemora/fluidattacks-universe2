# pylint: skip-file
from cryptography.hazmat.backends import (
    default_backend,
)
from cryptography.hazmat.primitives.ciphers import (
    algorithms,
    Cipher,
    modes,
)
import os

key = os.urandom(16)
iv = os.urandom(16)

# Noncompliant: vulnerable algorithms
tdes4 = Cipher(algorithms.TripleDES(key), mode=None, backend=default_backend())
bf3 = Cipher(algorithms.Blowfish(key), mode=None, backend=default_backend())
rc42 = Cipher(algorithms.ARC4(key), mode=None, backend=default_backend())

# Non Compliant: vulnerable modes
aes = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

# Compliant
aes2 = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
