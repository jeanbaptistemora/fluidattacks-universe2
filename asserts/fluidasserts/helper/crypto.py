# -*- coding: utf-8 -*-

"""
This module provide support for ``Cryptography`` operations.

:examples:
    - **Create an encrypted YAML file:**

      .. literalinclude:: example/crypto-create-yaml.py
          :linenos:
          :language: python

      `$ python3 crypto-create-yaml.py`:

      .. literalinclude:: example/crypto-create-yaml.py.out
          :language: yaml

      Save this file as **/resources/secrets.yml**

    - ``Use the encrypted YAML file in your exploits:``

      .. literalinclude:: example/crypto-use-yaml.exp
          :linenos:
          :language: python

      .. literalinclude:: example/crypto-use-yaml.exp.out
          :linenos:
          :language: python
"""

# standard imports
import io
import sys
import base64
from typing import Dict

# 3rd party imports
import yaml
from cryptography.fernet import Fernet


def _validate_key(key_b64) -> bytes:
    """Perform data quality and transformations over the key_b64."""
    secret_bytes: bytes = base64.b64decode(key_b64)
    secret_bytes_len: int = len(secret_bytes)

    # key_b64 quality
    if secret_bytes_len < 30:
        raise AssertionError('key_b64 must have at least 30 bytes, '
                             f'current: {secret_bytes_len}')
    if secret_bytes_len > 32:
        raise AssertionError('key_b64 must have at max 32 bytes, '
                             f'current: {secret_bytes_len}')

    # Fernet needs 32 bytes encoded with base 64 (url-safe)
    #   Append enough bytes to make it compliant
    secret_bytes += b'\x00' * (32 - secret_bytes_len)
    secret_bytes_len = len(secret_bytes)

    key_b64_url_safe: str = base64.urlsafe_b64encode(secret_bytes)

    return key_b64_url_safe


def _validate_secrets(secrets: Dict[str, str]) -> None:
    """Validate if secrets is a simple dictionary."""
    for key, val in secrets.items():
        if not isinstance(key, str) or not isinstance(val, str):
            raise AssertionError('secrets must be a dictionary of str -> str')


def create_encrypted_yaml(*,
                          key_b64: str,
                          secrets: Dict[str, str],
                          file: io.TextIOWrapper = sys.stdout):
    """
    Create an encrypted ``YAML`` file and print it to **file**.

    :param key_b64:
        - **Secret** used to encrypt the resultant ``YAML`` file
        - **an AWS secret key works out-of-the-box**
        - must be from 30 to 32 bytes encoded in standard base64.
    :param secrets: A **Dictionary** that maps strings to strings,
        note that only strings are supported,
        example: *{'user': 'Donald Knuth', 'password': 'asserts'}*
    :returns: Prints the content of the encrypted ``YAML`` to **file**,
        (defaults to sys.stdout).
    """
    secrets = secrets or {}

    # Data quality
    key_b64_url_safe: bytes = _validate_key(key_b64)
    _validate_secrets(secrets)

    # Encrypt
    secrets_encrypted: Dict[str, str] = {
        'secrets': {
            key: fernet.encrypt(val.encode()).decode()
            for fernet in (Fernet(key=key_b64_url_safe),)
            for key, val in secrets.items()
        }
    }

    # Dump it to YAML
    secrets_as_yaml: str = yaml.safe_dump(secrets_encrypted,
                                          width=64,
                                          default_flow_style=False,
                                          allow_unicode=True)

    # Flush it into file
    print(secrets_as_yaml, end=str(), file=file)

    return True


def create_decrypted_yaml(*,
                          key_b64: str,
                          input_file: str,
                          output_file=sys.stdout):
    """
    Decrypt an existing ``YAML`` file dumping the results to **output_file**.

    :param key_b64:
        - **Secret** used to decrypt the resultant ``YAML`` file
        - **an AWS secret key works out-of-the-box**
        - must be from 30 to 32 bytes encoded in standard base64.
    :param input_file: A path to the encrypted ``YAML``.
    :param output_file: A path or file-like object where the decrypted yaml
        will be put.
    :returns: Prints the content of the encrypted ``YAML`` to **output_file**,
        (defaults to sys.stdout).
    """
    # Data quality
    key_b64_url_safe: bytes = _validate_key(key_b64)

    # Load the input file as a dictionary from the YAML file
    with open(input_file) as file:
        input_file_content = file.read()
        input_file_yaml = yaml.safe_load(input_file_content)

    # Decrypt
    secrets_decrypted: Dict[str, str] = {
        'secrets': {
            key: fernet.decrypt(val.encode()).decode()
            for fernet in (Fernet(key=key_b64_url_safe),)
            for key, val in input_file_yaml['secrets'].items()
        }
    }

    # Dump it to YAML
    secrets_as_yaml: str = yaml.safe_dump(secrets_decrypted,
                                          width=64,
                                          default_flow_style=False,
                                          allow_unicode=True)

    # Flush it into file
    if isinstance(output_file, str):
        with open(output_file, 'w') as output_file_handle:
            print(secrets_as_yaml, end=str(), file=output_file_handle)
    else:
        print(secrets_as_yaml, end=str(), file=output_file)

    return True


class DecryptedYAML:
    """Decrypt an encrypted YAML and expose a dict interface to the secrets."""

    # pylint: disable=too-few-public-methods

    def __init__(self, *, key_b64: str, encrypted_yaml_path: str):
        """Instantiate the class from the yaml path and the secret."""
        # Fernet needs an special key derived from the key_b64 provided
        self.key_b64_url_safe = _validate_key(key_b64)

        # Load the encrypted yaml
        with open(encrypted_yaml_path, mode='rb') as handle:
            encrypted_yaml_content: str = handle.read().decode()
            encrypted_yaml: Dict[str, str] = \
                yaml.safe_load(encrypted_yaml_content)

        self.encrypted_data = encrypted_yaml['secrets']

        # Decrypt it and expose it
        self.decrypted_data = {
            key: fernet.decrypt(val.encode()).decode()
            for fernet in (Fernet(key=self.key_b64_url_safe),)
            for key, val in self.encrypted_data.items()
        }

    def __getitem__(self, key) -> str:
        """Return a decrypted key from the encrypted yaml file."""
        return self.decrypted_data[key]
