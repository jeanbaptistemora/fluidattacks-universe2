# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from http_headers.types import (
    AcceptHeader,
)
from operator import (
    methodcaller,
)
from typing import (
    List,
    Optional,
)


def _is_accept(name: str) -> bool:
    return name.lower() == "accept"


def parse(line: str) -> Optional[AcceptHeader]:
    portions: List[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    name, value = portions

    if not _is_accept(name):
        return None

    return AcceptHeader(
        name=name,
        value=value,
    )
