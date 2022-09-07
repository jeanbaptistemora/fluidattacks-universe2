# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from purity.v2.pure_iter.factory import (
    from_flist,
    from_range,
    infinite_range,
)
from tests.v2.pure_iter._utils import (
    assert_immutability,
    assert_immutability_inf,
)


def test_flist() -> None:
    items = tuple(range(10))
    assert_immutability(from_flist(items))


def test_range() -> None:
    assert_immutability(from_range(range(10)))


def test_inf_range() -> None:
    assert_immutability_inf(infinite_range(3, 5))
