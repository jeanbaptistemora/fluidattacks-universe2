# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from target_snowflake.snowflake_client.db import (
    DbManager,
    SchemaId,
)
from target_snowflake.snowflake_client.sql_client import (
    Identifier,
)
from typing import (
    Callable,
)


@dataclass(frozen=True)
class LoadingStrategy:
    _target: SchemaId
    _manager: DbManager

    @property
    def _backup_schema(self) -> SchemaId:
        return SchemaId(
            Identifier.from_raw(self._target.name.sql_identifier + "_backup")
        )

    @property
    def _loading_schema(self) -> SchemaId:
        return SchemaId(
            Identifier.from_raw(self._target.name.sql_identifier + "_loading")
        )

    def _post_upload(self) -> Cmd[None]:
        _do_nothing = Cmd.from_cmd(lambda: None)
        drop_backup = self._manager.exist(self._backup_schema).bind(
            lambda b: self._manager.delete_cascade(self._backup_schema)
            if b
            else _do_nothing
        )
        rename_old = self._manager.exist(self._target).bind(
            lambda b: self._manager.rename(self._target, self._backup_schema)
            if b
            else _do_nothing
        )
        rename_loading = self._manager.exist(self._loading_schema).bind(
            lambda b: self._manager.rename(self._loading_schema, self._target)
            if b
            else _do_nothing
        )
        return drop_backup + rename_old + rename_loading

    def main(self, procedure: Callable[[SchemaId], Cmd[None]]) -> Cmd[None]:
        recreate = self._manager.recreate_cascade(self._loading_schema)
        upload = procedure(self._loading_schema)
        return recreate + upload + self._post_upload()
