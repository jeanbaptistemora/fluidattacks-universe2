# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.helper.crypto."""

# standard imports
from tempfile import NamedTemporaryFile
from typing import Any, Dict

# Third parties libraries
import pytest

# local imports
from fluidasserts.helper import crypto


#
# Constants
#

key_b64_bad_29: str = 'dGVzdHN0ZXN0c3Rlc3RzdGVzdHN0ZXN0c3Rlcwo='
key_b64_good__: str = 'dGVzdHN0ZXN0c3Rlc3RzdGVzdHN0ZXN0c3Rlc3RzCg=='
key_b64_bad_33: str = 'dGVzdHN0ZXN0c3Rlc3RzdGVzdHN0ZXN0c3Rlc3RzdGUK'

secrets_good: Dict[str, str] = {
    'user': 'fluid',
    'pass': 'asserts',
}

secrets_bad: Dict[str, Any] = {
    # Only instances of str -> str are supported
    'user': 'fluid',
    'passwords': [
        'fluid',
        'asserts'
    ]
}

secrets_file_path: str = 'test/static/helper/crypto/credentials.yml'

#
# Tests
#


def test_ok():
    """Test a successful use."""
    with NamedTemporaryFile(mode='w') as file:

        # Create an encrypted yaml file
        assert crypto.create_encrypted_yaml(key_b64=key_b64_good__,
                                            secrets=secrets_good,
                                            file=file)

        file.seek(0)

        # Load the encrypted yaml file
        secrets = crypto.DecryptedYAML(key_b64=key_b64_good__,
                                       encrypted_yaml_path=file.name)

        # Verify data integrity
        assert secrets['user'] == secrets_good['user']


def test_read():
    """Test a normal use based on the file."""
    # Load the encrypted yaml file
    secrets = crypto.DecryptedYAML(key_b64=key_b64_good__,
                                   encrypted_yaml_path=secrets_file_path)

    # Verify data integrity
    assert secrets['user'] == secrets_good['user']


def test_bad():
    """Test a bad use."""
    with pytest.raises(AssertionError):
        assert crypto.create_encrypted_yaml(key_b64=key_b64_bad_29,
                                            secrets=secrets_good)

    with pytest.raises(AssertionError):
        assert crypto.create_encrypted_yaml(key_b64=key_b64_bad_33,
                                            secrets=secrets_good)

    with pytest.raises(AssertionError):
        assert crypto.create_encrypted_yaml(key_b64=key_b64_good__,
                                            secrets=secrets_bad)
