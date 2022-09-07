# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


def is_key_sensitive(key: str) -> bool:
    return any(
        key.lower().endswith(suffix)
        for suffix in [
            "key",
            "pass",
            "passwd",
            "user",
            "username",
        ]
    )
