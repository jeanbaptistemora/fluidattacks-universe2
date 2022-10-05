# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    FrozenList,
    Maybe,
    PureIter,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from target_snowflake.snowflake_client.sql_client import (
    RowData,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")
_D = TypeVar("_D")


def _get_index(items: FrozenList[_T], index: int, default: _D) -> _T | _D:
    try:
        return items[index]
    except IndexError:
        return default


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class RowsPackage:
    _inner: _Private = field(repr=False, hash=False, compare=False)
    row_length: int
    rows: PureIter[RowData]

    @staticmethod
    def new(rows: FrozenList[RowData]) -> Maybe[RowsPackage]:
        return Maybe.from_optional(_get_index(rows, 1, None)).map(
            lambda r: RowsPackage(_Private(), len(r.data), from_flist(rows))
        )
