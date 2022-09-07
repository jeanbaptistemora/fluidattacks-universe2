# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from functools import (
    lru_cache,
)
import re
from toolbox.utils import (
    generic,
)
from toolbox.utils.function import (
    shield,
)
from typing import (
    Match,
    Optional,
)


@shield()
@lru_cache(maxsize=None, typed=True)
def main() -> str:
    """Return the group name from the last commmit msg."""
    group: str = ""

    summary: str = generic.get_change_request_summary()
    regex: str = r"\w+\(\w+\):\s+(?:#\d+(?:\.\d+)?\s+)?(?P<group>\w+)"

    regex_match: Optional[Match] = re.search(regex, summary)
    if regex_match:
        group = regex_match.groupdict()["group"]

    return group
