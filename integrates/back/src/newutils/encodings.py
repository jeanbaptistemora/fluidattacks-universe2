# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


def safe_encode(string: str) -> str:
    """Turn a utf-8 string into a string of [a-z0-9] characters."""
    return string.encode("utf-8").hex().lower()


def safe_decode(hexstr: str) -> str:
    """Inverse of safe_encode."""
    return bytes.fromhex(hexstr).decode("utf-8")
