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
    """Wraps a loading operation (over a schema) with custom pre and post upload operations"""

    _procedure: _Patch[Callable[[PackagedSinger], Cmd[None]]]

    @staticmethod
    def new(procedure: Callable[[PackagedSinger], Cmd[None]]) -> SingerLoader:
        return SingerLoader(_Patch(procedure))

    def handle(self, msg: PackagedSinger) -> Cmd[None]:
        return self._procedure.inner(msg)
