# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    Iterable,
    List,
    Optional,
    Tuple,
)


def iter_with_next(
    values: List[str], last: Optional[str]
) -> Iterable[Tuple[str, Optional[str]]]:
    for value, next_value in zip(values, values[1:]):
        yield value, next_value
    yield values[-1], last
