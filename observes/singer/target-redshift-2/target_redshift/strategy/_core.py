from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from redshift_client.id_objs import (
    SchemaId,
)
from typing import (
    Callable,
    Generic,
    TypeVar,
)

_T = TypeVar("_T")
LoadProcedure = Callable[[SchemaId], Cmd[None]]


@dataclass(frozen=True)
class _Patch(Generic[_T]):
    inner: _T


@dataclass(frozen=True)
class LoadingStrategy:
    """Wraps a loading operation (over a schema) with custom pre and post upload operations"""

    _main: _Patch[Callable[[LoadProcedure], Cmd[None]]]

    @staticmethod
    def new(main: Callable[[LoadProcedure], Cmd[None]]) -> LoadingStrategy:
        return LoadingStrategy(_Patch(main))

    def main(self, procedure: LoadProcedure) -> Cmd[None]:
        return self._main.inner(procedure)
