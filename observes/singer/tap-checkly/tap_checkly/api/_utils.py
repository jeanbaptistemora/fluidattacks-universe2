# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity import (
    Cmd,
    FrozenList,
    Stream,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
    until_none,
)
from tap_checkly._utils import (
    ExtendedUnfolder,
    isoparse,
    switch_maybe,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")


def paginate_all(
    list_items: Callable[[int], Cmd[FrozenList[_T]]]
) -> Stream[_T]:
    return (
        infinite_range(1, 1)
        .map(list_items)
        .transform(lambda x: from_piter(x))
        .map(lambda i: i if bool(i) else None)
        .transform(lambda x: until_none(x))
        .map(lambda x: from_flist(x))
        .transform(lambda x: chain(x))
    )


__all__ = [
    "isoparse",
    "switch_maybe",
    "ExtendedUnfolder",
]
