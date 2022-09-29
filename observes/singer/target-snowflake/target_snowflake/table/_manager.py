# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from ._core import (
    Table,
)
from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    Cmd,
    PureIter,
)
from target_snowflake.sql_client import (
    RowData,
)


class UpperMethods(ABC):
    @abstractmethod
    def insert(
        self,
        table_def: Table,
        items: PureIter[RowData],
        limit: int,
    ) -> Cmd[None]:
        pass


@dataclass(frozen=True)
class TableManager:
    _upper: UpperMethods = field(repr=False, hash=False, compare=False)

    def insert(
        self,
        table_def: Table,
        items: PureIter[RowData],
        limit: int,
    ) -> Cmd[None]:
        return self._upper.insert(table_def, items, limit)
