# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from http_headers.types import (
    ContentEncodingHeader,
)
from operator import (
    methodcaller,
)
from typing import (
    List,
    Optional,
)


def _is_content_encoding(name: str) -> bool:
    return name.lower() == "content-encoding"


def parse(line: str) -> Optional[ContentEncodingHeader]:
    portions: List[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    name, value = portions

    if not _is_content_encoding(name):
        return None

    return ContentEncodingHeader(
        name=name,
        value=value,
    )
