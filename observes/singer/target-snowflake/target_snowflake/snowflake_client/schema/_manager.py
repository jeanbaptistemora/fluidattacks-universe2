# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

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
from target_snowflake.snowflake_client.schema import (
    TableId,
    TableObj,
)
from target_snowflake.snowflake_client.sql_client import (
    RowData,
)
from target_snowflake.snowflake_client.table import (
    Table,
    TableManager,
    UpperMethods as TableUpperMethods,
)
from typing import (
    FrozenSet,
)


class UpperMethods(ABC):
    @abstractmethod
    def table_ids(self) -> Cmd[FrozenSet[TableId]]:
        pass

    @abstractmethod
    def create(self, table_obj: TableObj, if_not_exist: bool) -> Cmd[None]:
        pass

    @abstractmethod
    def create_like(self, blueprint: TableId, new: TableId) -> Cmd[None]:
        pass

    @abstractmethod
    def rename(self, old: TableId, new: TableId) -> Cmd[None]:
        pass

    @abstractmethod
    def _delete(self, target: TableId, cascade: bool) -> Cmd[None]:
        pass

    @abstractmethod
    def append_table(self, source: TableId, target: TableId) -> Cmd[None]:
        pass

    @abstractmethod
    def insert(
        self,
        table_id: TableId,
        table_def: Table,
        items: PureIter[RowData],
        limit: int,
    ) -> Cmd[None]:
        pass


@dataclass(frozen=True)
class SchemaManager:
    _upper: UpperMethods = field(repr=False, hash=False, compare=False)

    def table_ids(self) -> Cmd[FrozenSet[TableId]]:
        return self._upper.table_ids()

    def create(self, table_obj: TableObj, if_not_exist: bool) -> Cmd[None]:
        return self._upper.create(table_obj, if_not_exist)

    def create_like(self, blueprint: TableId, new: TableId) -> Cmd[None]:
        return self._upper.create_like(blueprint, new)

    def rename(self, old: TableId, new: TableId) -> Cmd[None]:
        return self._upper.rename(old, new)

    def _delete(self, target: TableId, cascade: bool) -> Cmd[None]:
        return self._upper._delete(target, cascade)

    def delete(self, table_id: TableId) -> Cmd[None]:
        return self._delete(table_id, False)

    def delete_cascade(self, table_id: TableId) -> Cmd[None]:
        return self._delete(table_id, True)

    def append_table(self, source: TableId, target: TableId) -> Cmd[None]:
        return self._upper.append_table(source, target)

    def table_manager(self, table: TableId) -> TableManager:
        class _ConcreteMethods(TableUpperMethods):
            def insert(
                s,
                table_def: Table,
                items: PureIter[RowData],
                limit: int,
            ) -> Cmd[None]:
                return self._upper.insert(table, table_def, items, limit)

        return TableManager(_ConcreteMethods())
