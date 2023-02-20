from __future__ import (
    annotations,
)

from . import (
    _group_org,
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
    ResultE,
)
from typing import (
    FrozenSet,
)


@dataclass(frozen=True)
class _ArmToken:
    token: str


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class ArmToken:
    _inner: _ArmToken

    @staticmethod
    def new(token: str) -> ArmToken:
        return ArmToken(_ArmToken(token))

    def get(
        self, key: _Private  # pylint: disable=unused-argument # NOSONAR
    ) -> str:
        # key is to disable that token can be getted anywhere
        return self._inner.token

    def __repr__(self) -> str:
        return "[masked]"


@dataclass(frozen=True)
class _ArmClient:
    client: GraphQlAsmClient


@dataclass(frozen=True)
class ArmClient:
    _inner: _ArmClient

    @staticmethod
    def new(token: ArmToken) -> Cmd[ArmClient]:
        return (
            GraphQlAsmClient.new(token.get(_Private()))
            .map(_ArmClient)
            .map(ArmClient)
        )

    def get_ignored_paths(self, group: str) -> Cmd[FrozenSet[IgnoredPath]]:
        return _ignored_paths.get_ignored_paths(self._inner.client, group)

    def get_org(self, group: str) -> Cmd[ResultE[str]]:
        return _group_org.get_org(self._inner.client, group)


__all__ = [
    "IgnoredPath",
]
