# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from utils.crypto import (
    is_vulnerable_cipher,
)


def is_cipher_vulnerable(transformation: str) -> bool:
    if not isinstance(transformation, str):
        return False
    alg, mode, pad, *_ = (
        transformation.lower().replace('"', "") + "///"
    ).split("/", 3)

    return is_vulnerable_cipher(alg, mode, pad)
