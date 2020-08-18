# Standard library
import hashlib
import hmac

# Third party libraries
from aioextensions import (
    in_process,
)

# Constants
HASH = hashlib.blake2b  # https://blake2.net/


def _get_hash(stream: bytes) -> bytes:
    digestor = HASH()
    digestor.update(stream)

    return digestor.digest()


async def get_hash(stream: bytes) -> bytes:
    return await in_process(_get_hash, stream)


def _get_hmac(key: bytes, stream: bytes) -> bytes:
    return hmac.new(key, msg=stream, digestmod=HASH).digest()


async def get_hmac(key: bytes, stream: bytes) -> bytes:
    return await in_process(_get_hmac, key, stream)
