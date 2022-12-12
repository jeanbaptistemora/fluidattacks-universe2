from __future__ import (
    annotations,
)

from . import (
    _ignored_paths,
)
from ._ignored_paths import (
    IgnoredPath,
)
from ._raw_client import (
    GraphQlAsmClient,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
)


@dataclass(frozen=True)
class _ArmClient:
    client: GraphQlAsmClient


@dataclass(frozen=True)
class ArmClient:
    _inner: _ArmClient

    @staticmethod
    def new(token: str) -> Cmd[ArmClient]:
        return GraphQlAsmClient.new(token).map(_ArmClient).map(ArmClient)

    def get_ignored_paths(self, group: str) -> Cmd[FrozenList[IgnoredPath]]:
        return _ignored_paths.get_ignored_paths(self._inner.client, group)
