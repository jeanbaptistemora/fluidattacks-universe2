# -*- coding: utf-8 -*-

"""This module provide support for ``Cryptography`` operations."""

# standard imports
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


def create(*, key_b64: str, secrets: Dict[str, str], file=sys.stdout) -> bool:
    """Create an encrypted YAML file and print it to stdout."""
    secrets = secrets or {}

    # Data quality
    key_b64_url_safe: bytes = _validate_key(key_b64)
    _validate_secrets(secrets)

    # Conversions
    secrets_encrypted: Dict[str, str] = {
        'secrets': {
            key: fernet.encrypt(val.encode()).decode()
            for key, val in secrets.items()
            for fernet in (Fernet(key=key_b64_url_safe),)
        }
    }

    secrets_as_yaml: str = yaml.safe_dump(secrets_encrypted,
                                          width=64,
                                          default_flow_style=False,
                                          allow_unicode=True)

    # Encrypt
    print(secrets_as_yaml, end=str(), file=file)

    return True


class Secrets:
    """Dict-like object to programatically access an encrypted YAML."""

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
            for key, val in self.encrypted_data.items()
            for fernet in (Fernet(key=self.key_b64_url_safe),)
        }

    def __getitem__(self, key) -> str:
        """Return an decrypted key from the encrypted yaml file."""
        return self.decrypted_data[key]
