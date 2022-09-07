# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

"""Main module to build and check Assert Exploits."""


import re
from typing import (
    Any,
)

# Compiled regular expresions
RE_SPACE_CHARS = re.compile(r"\s", flags=re.M)
RE_NOT_ALLOWED_CHARS = re.compile(r"[^a-zá-úñÁ-ÚÑA-Z0-9\s,._]", flags=re.M)


def sanitize_string(string: Any) -> str:
    """Sanitize the string to allow only certain values."""
    string = RE_NOT_ALLOWED_CHARS.sub("", str(string)[0:512])
    string = RE_SPACE_CHARS.sub(" ", string)
    string = string.strip()
    return string
