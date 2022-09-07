# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import contextlib
from datetime import (
    datetime,
    timezone,
)
from http_headers.common import (
    parse_key_value,
)
from http_headers.types import (
    DateHeader,
)
from typing import (
    Optional,
)

# Date: <day-name>, <day> <month> <year> <hour>:<minute>:<second> GMT
FORMAT: str = "%a, %d %b %Y %H:%M:%S GMT"


def _is_date(name: str) -> bool:
    return name.lower() == "date"


def parse(line: str) -> Optional[DateHeader]:
    if data := parse_key_value(
        is_header=_is_date,
        line=line,
    ):
        with contextlib.suppress(ValueError):
            return DateHeader(
                name=data[0],
                date=datetime.strptime(data[1], FORMAT).replace(
                    tzinfo=timezone.utc,
                ),
            )

    return None
