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
from target_snowflake.snowflake_client._rows_package import (
    RowsPackage,
)
from target_snowflake.snowflake_client.db import (
    SchemaId,
)
from target_snowflake.snowflake_client.schema import (
    SchemaManager,
    TableId,
    TableObj,
    UpperMethods as SchemaUpperMethods,
)
from target_snowflake.snowflake_client.sql_client import (
    Cursor,
    RowData,
)
from target_snowflake.snowflake_client.table import (
    Table,
)
from typing import (
    FrozenSet,
)


@dataclass(frozen=True)
class DbTableId:
    schema: SchemaId
    table: TableId


class UpperMethods(ABC):
    @abstractmethod
    def create_table(
        self, table_id: DbTableId, table: Table, if_not_exist: bool
    ) -> Cmd[None]:
        pass

    @abstractmethod
    def create_table_like(
        self, blueprint: DbTableId, new_table: DbTableId
    ) -> Cmd[None]:
        pass

    @abstractmethod
    def exist_schema(self, schema: SchemaId) -> Cmd[bool]:
        pass

    @abstractmethod
    def rename_table(self, old: DbTableId, new: DbTableId) -> Cmd[None]:
        pass

    @abstractmethod
    def delete_table(self, target: DbTableId, cascade: bool) -> Cmd[None]:
        pass

    @abstractmethod
    def table_ids(self, schema: SchemaId) -> Cmd[FrozenSet[TableId]]:
        pass

    @abstractmethod
    def rename_schema(self, old: SchemaId, new: SchemaId) -> Cmd[None]:
        pass

    @abstractmethod
    def delete_schema(self, target: SchemaId, cascade: bool) -> Cmd[None]:
        pass

    @abstractmethod
    def create_schema(
        self, schema: SchemaId, if_not_exist: bool = False
    ) -> Cmd[None]:
        pass

    @abstractmethod
    def append_table(self, source: DbTableId, target: DbTableId) -> Cmd[None]:
        pass

    @abstractmethod
    def insert(
        self,
        table_id: DbTableId,
        table_def: Table,
        items: RowsPackage,
    ) -> Cmd[None]:
        pass


@dataclass(frozen=True)
class DbManager:
    _cursor: Cursor
    _upper: UpperMethods = field(repr=False, hash=False, compare=False)

    def exist(self, schema: SchemaId) -> Cmd[bool]:
        return self._upper.exist_schema(schema)

    def delete(self, schema: SchemaId) -> Cmd[None]:
        return self._upper.delete_schema(schema, False)

    def delete_cascade(self, schema: SchemaId) -> Cmd[None]:
        return self._upper.delete_schema(schema, False)

    def rename(self, old: SchemaId, new: SchemaId) -> Cmd[None]:
        return self._upper.rename_schema(old, new)

    def create(
        self, schema: SchemaId, if_not_exist: bool = False
    ) -> Cmd[None]:
        return self._upper.create_schema(schema, if_not_exist)

    def _recreate(self, schema: SchemaId, cascade: bool) -> Cmd[None]:
        nothing = Cmd.from_cmd(lambda: None)
        return self.exist(schema).bind(
            lambda b: self._upper.delete_schema(schema, cascade)
            if b
            else nothing
        ) + self.create(schema)

    def recreate(self, schema: SchemaId) -> Cmd[None]:
        return self._recreate(schema, False)

    def recreate_cascade(self, schema: SchemaId) -> Cmd[None]:
        return self._recreate(schema, True)

    def schema_manager(self, schema: SchemaId) -> SchemaManager:
        def _table_path(table: TableId) -> DbTableId:
            return DbTableId(schema, table)

        class _ConcreteMethods(SchemaUpperMethods):
            def table_ids(s) -> Cmd[FrozenSet[TableId]]:
                return self._upper.table_ids(schema)

            def create(
                s, table_obj: TableObj, if_not_exist: bool
            ) -> Cmd[None]:
                return self._upper.create_table(
                    _table_path(table_obj.id_obj),
                    table_obj.table,
                    if_not_exist,
                )

            def create_like(s, blueprint: TableId, new: TableId) -> Cmd[None]:
                return self._upper.create_table_like(
                    _table_path(blueprint), _table_path(new)
                )

            def rename(s, old: TableId, new: TableId) -> Cmd[None]:
                return self._upper.rename_table(
                    _table_path(old), _table_path(new)
                )

            def _delete(s, target: TableId, cascade: bool) -> Cmd[None]:
                return self._upper.delete_table(_table_path(target), cascade)

            def append_table(s, source: TableId, target: TableId) -> Cmd[None]:
                return self._upper.append_table(
                    _table_path(source), _table_path(target)
                )

            def insert(
                s,
                table_id: TableId,
                table_def: Table,
                items: RowsPackage,
            ) -> Cmd[None]:
                return self._upper.insert(
                    _table_path(table_id), table_def, items
                )

        return SchemaManager(_ConcreteMethods())
