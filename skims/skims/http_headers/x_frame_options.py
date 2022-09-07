# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from http_headers.types import (
    XFrameOptionsHeader,
)
from operator import (
    methodcaller,
)
from typing import (
    List,
    Optional,
)


def _is_x_frame_options(name: str) -> bool:
    return name.lower() == "x-frame-options"


def parse(line: str) -> Optional[XFrameOptionsHeader]:
    portions: List[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    if len(portions) != 2:
        return None

    name, value = portions

    if not _is_x_frame_options(name):
        return None

    return XFrameOptionsHeader(
        name=name,
        value=value.lower(),
    )
