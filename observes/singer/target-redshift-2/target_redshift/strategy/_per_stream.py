# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from ._core import (
    LoadingStrategy,
    LoadProcedure,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from fa_purity.pure_iter.factory import (
    pure_map,
)
from fa_purity.pure_iter.transform import (
    consume,
)
from redshift_client.id_objs import (
    SchemaId,
    TableId,
)
from redshift_client.schema.client import (
    SchemaClient,
)
from redshift_client.table.client import (
    TableClient,
)
from typing import (
    FrozenSet,
)


@dataclass(frozen=True)
class RecreatePerStream:
    _target: SchemaId
    _client: SchemaClient
    _client_2: TableClient
    persistent_tables: FrozenSet[str]

    @property
    def _backup_schema(self) -> SchemaId:
        return SchemaId(f"{self._target.name}_backup")

    @property
    def _loading_schema(self) -> SchemaId:
        return SchemaId(f"{self._target.name}_loading")

    def _backup(self) -> Cmd[None]:
        """migrate non-persistent tables, target -> backup"""

        def _migrate(table: TableId) -> Cmd[None]:
            if table.name in self.persistent_tables:
                return Cmd.from_cmd(lambda: None)
            return self._client_2.migrate(
                table, TableId(self._backup_schema, table.name)
            )

        return self._client.table_ids(self._target).bind(
            lambda tables: consume(pure_map(_migrate, tuple(tables)))
        )

    def _move_data(self) -> Cmd[None]:
        """
        loading -> target
        - migrate non-persistent tables
        - move persistent tables
        """

        def _action(table: TableId) -> Cmd[None]:
            if table.name in self.persistent_tables:
                return self._client_2.move(
                    table, TableId(self._target, table.name)
                )
            return self._client_2.migrate(
                table, TableId(self._target, table.name)
            )

        return self._client.table_ids(self._loading_schema).bind(
            lambda tables: consume(pure_map(_action, tuple(tables)))
        )

    def main(self, procedure: LoadProcedure) -> Cmd[None]:
        recreate = self._client.recreate_cascade(self._loading_schema)
        upload = procedure(self._loading_schema)
        _post_upload = self._backup() + self._move_data()
        return recreate + upload + _post_upload

    @property
    def strategy(self) -> LoadingStrategy:
        return LoadingStrategy.new(self.main)
