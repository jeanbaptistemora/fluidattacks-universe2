from contextlib import (
    suppress,
)
from utils.crypto import (
    is_vulnerable_cipher,
)


def is_cipher_vulnerable(transformation: str) -> bool:
    if not isinstance(transformation, str):
        return False
    alg, mode, pad, *_ = (
        transformation.lower().replace('"', "") + "---"
    ).split("-", 3)

    with suppress(ValueError):
        # the padding can be the mode
        # AES-256-ECB
        int(mode)
        mode = pad

    return is_vulnerable_cipher(alg, mode, pad)
