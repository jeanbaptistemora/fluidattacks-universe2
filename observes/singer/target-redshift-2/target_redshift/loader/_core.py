# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from target_redshift.grouper import (
    PackagedSinger,
)
from typing import (
    Callable,
    Generic,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class _Patch(Generic[_T]):
    inner: _T


@dataclass(frozen=True)
class SingerLoader:
    _procedure: _Patch[Callable[[SchemaId, PackagedSinger], Cmd[None]]]

    @staticmethod
    def new(
        procedure: Callable[[SchemaId, PackagedSinger], Cmd[None]]
    ) -> SingerLoader:
        return SingerLoader(_Patch(procedure))

    def handle(self, schema: SchemaId, msg: PackagedSinger) -> Cmd[None]:
        return self._procedure.inner(schema, msg)
