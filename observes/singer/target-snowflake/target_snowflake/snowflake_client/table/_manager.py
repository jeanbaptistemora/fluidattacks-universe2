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
)
from target_snowflake.snowflake_client._rows_package import (
    RowsPackage,
)


class UpperMethods(ABC):
    @abstractmethod
    def insert(
        self,
        table_def: Table,
        items: RowsPackage,
    ) -> Cmd[None]:
        pass


@dataclass(frozen=True)
class TableManager:
    _upper: UpperMethods = field(repr=False, hash=False, compare=False)

    def insert(
        self,
        table_def: Table,
        items: RowsPackage,
    ) -> Cmd[None]:
        return self._upper.insert(table_def, items)
