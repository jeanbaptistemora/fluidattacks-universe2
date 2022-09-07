# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from purity.v2.pure_iter.factory import (
    from_range,
)
from tests.v2.pure_iter._utils import (
    assert_immutability,
)


def test_map() -> None:
    items = from_range(range(10)).map(lambda i: i + 1)
    assert_immutability(items)


def test_chunked() -> None:
    items = from_range(range(10)).chunked(2)
    assert_immutability(items)
