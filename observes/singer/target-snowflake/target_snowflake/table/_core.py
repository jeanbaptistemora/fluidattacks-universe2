# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity.result import (
    Result,
    ResultE,
)
from target_snowflake.column import (
    Column,
    ColumnId,
)
from typing import (
    Callable,
    FrozenSet,
)


@dataclass(frozen=True)
class _Private:
    # item for making default Table constructor private
    pass


@dataclass(frozen=True)
class Table:
    _inner: _Private
    order: FrozenList[ColumnId]
    columns: FrozenDict[ColumnId, Column]
    primary_keys: FrozenSet[ColumnId]

    @staticmethod
    def new(
        order: FrozenList[ColumnId],
        columns: FrozenDict[ColumnId, Column],
        primary_keys: FrozenSet[ColumnId],
    ) -> ResultE[Table]:
        in_columns: Callable[[ColumnId], bool] = lambda k: k in columns
        non_duplicated = len(frozenset(order)) == len(order)
        if not non_duplicated:
            return Result.failure(
                Exception("order list must have unique `ColumnId` objs")
            )
        if all(map(in_columns, primary_keys)):
            table = Table(_Private(), order, columns, primary_keys)
            return Result.success(table)
        return Result.failure(Exception("All primary keys must be in columns"))
