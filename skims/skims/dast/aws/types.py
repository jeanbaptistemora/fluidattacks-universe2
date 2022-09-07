# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    Any,
    NamedTuple,
    Tuple,
)


class Location(NamedTuple):
    arn: str
    access_patterns: Tuple[str, ...]
    description: str
    values: Tuple[Any, ...]
