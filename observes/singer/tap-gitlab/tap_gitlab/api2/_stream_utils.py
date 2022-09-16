# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Maybe,
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
    until_empty,
)
from tap_gitlab.api2._raw.page import (
    Page,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class GenericStream:
    _start_page: int
    _per_page: int

    def generic_stream(
        self,
        get_page: Callable[[Page], Cmd[_T]],
        is_empty: Callable[[_T], Maybe[_T]],
    ) -> Stream[_T]:
        return (
            infinite_range(self._start_page, 1)
            .map(lambda i: Page.new_page(i, self._per_page).unwrap())
            .map(get_page)
            .transform(lambda x: from_piter(x))
            .map(is_empty)
            .transform(until_empty)
        )

    def generic_page_stream(
        self,
        get_page: Callable[[Page], Cmd[FrozenList[_T]]],
        is_empty: Callable[[FrozenList[_T]], Maybe[FrozenList[_T]]],
    ) -> Stream[_T]:
        return (
            self.generic_stream(
                get_page,
                is_empty,
            )
            .map(lambda x: from_flist(x))
            .transform(lambda x: chain(x))
        )

    @staticmethod
    def _is_empty(items: FrozenList[_T]) -> Maybe[FrozenList[_T]]:
        return Maybe.from_optional(items if items else None)
