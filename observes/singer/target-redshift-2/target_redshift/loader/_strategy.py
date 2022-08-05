from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from redshift_client.id_objs import (
    SchemaId,
)
from redshift_client.schema.client import (
    SchemaClient,
)
from typing import (
    Callable,
)


@dataclass(frozen=True)
class LoadingStrategy:
    _target: SchemaId
    _client: SchemaClient

    @property
    def _backup_schema(self) -> SchemaId:
        return SchemaId(f"{self._target.name}_backup")

    @property
    def _loading_schema(self) -> SchemaId:
        return SchemaId(f"{self._target.name}_loading")

    def _post_upload(self) -> Cmd[None]:
        _do_nothing = Cmd.from_cmd(lambda: None)
        drop_backup = self._client.exist(self._backup_schema).bind(
            lambda b: self._client.delete_cascade(self._backup_schema)
            if b
            else _do_nothing
        )
        rename_old = self._client.exist(self._target).bind(
            lambda b: self._client.rename(self._target, self._backup_schema)
            if b
            else _do_nothing
        )
        rename_loading = self._client.exist(self._loading_schema).bind(
            lambda b: self._client.rename(self._loading_schema, self._target)
            if b
            else _do_nothing
        )
        return drop_backup + rename_old + rename_loading

    def main(self, procedure: Callable[[SchemaId], Cmd[None]]) -> Cmd[None]:
        recreate = self._client.recreate_cascade(self._loading_schema)
        upload = procedure(self._loading_schema)
        return recreate + upload + self._post_upload()
