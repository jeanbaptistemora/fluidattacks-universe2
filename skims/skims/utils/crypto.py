from aioextensions import (
    in_process,
)
import csv
import hashlib
import hmac
from typing import (
    Dict,
    Optional,
)
from utils.ctx import (
    CIPHER_SUITES_PATH,
)

# Constants
HASH = hashlib.blake2b  # https://blake2.net/
_CIPHER_SUITES_IANA: Dict[str, bool] = {}
"""Mapping from I.A.N.A. cipher suites to boolean indicating cipher safety."""
_CIPHER_SUITES_OPEN_SSL: Dict[str, bool] = {}
"""Mapping from OpenSSL cipher suites to boolean indicating cipher safety."""


def get_hash(stream: bytes) -> bytes:
    digestor = HASH()
    digestor.update(stream)

    return digestor.digest()


def _get_hmac(key: bytes, stream: bytes) -> bytes:
    return hmac.new(key, msg=stream, digestmod=HASH).digest()


async def get_hmac(key: bytes, stream: bytes) -> bytes:
    return await in_process(_get_hmac, key, stream)


def _load_static_data() -> None:
    with open(CIPHER_SUITES_PATH) as cipher_suites_file:
        for row in csv.DictReader(cipher_suites_file):
            # Parse safe column
            if row["safe"] == "yes":
                safe: bool = True
            elif row["safe"] == "no":
                safe = False
            else:
                raise NotImplementedError(row["safe"])

            # Match the names
            for column, data in [
                ("name_iana", _CIPHER_SUITES_IANA),
                ("name_open_ssl", _CIPHER_SUITES_OPEN_SSL),
            ]:
                if name := row[column]:
                    data[name] = safe


def is_iana_cipher_suite_vulnerable(identifier: str) -> bool:
    safe: bool = _CIPHER_SUITES_IANA.get(identifier.lower(), True)

    return not safe


def is_open_ssl_cipher_suite_vulnerable(identifier: str) -> bool:
    safe: bool = _CIPHER_SUITES_OPEN_SSL.get(identifier.lower(), True)

    return not safe


def is_vulnerable_cipher(
    alg: str, mode: str, pad: Optional[str] = None
) -> bool:
    pad = pad or ""
    alg = alg.lower()
    mode = mode.lower()
    pad = pad.lower()
    return any(
        (
            alg == "aes" and mode == "ecb",
            alg == "aes" and mode == "cbc" and pad and pad != "nopadding",
            alg == "blowfish",
            alg == "bf",
            alg == "des",
            alg == "desede",
            alg == "rc2",
            alg == "rc4",
            alg == "rsa" and "oaep" not in pad,
        )
    )


# Side effects
_load_static_data()
