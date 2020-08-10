# Standard library
import hashlib
import hmac

# Third party libraries
from aioextensions import (
    unblock_cpu,
)

# Constants
HASH = hashlib.sha3_512
DIGEST_SIZE: int = 64


def _get_hash(stream: bytes) -> bytes:
    digestor = HASH()
    digestor.update(stream)

    return digestor.digest()


async def get_hash(stream: bytes) -> bytes:
    return await unblock_cpu(_get_hash, stream)


def _get_hmac(key: bytes, stream: bytes) -> bytes:
    return hmac.new(key, msg=stream, digestmod=HASH).digest()


async def get_hmac(key: bytes, stream: bytes) -> bytes:
    return await unblock_cpu(_get_hmac, key, stream)
