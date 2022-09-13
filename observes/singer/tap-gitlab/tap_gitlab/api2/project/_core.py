# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from urllib.parse import (
    quote,
    unquote,
)


@dataclass(frozen=True)
class _ProjectId:
    proj_id: str | int


@dataclass(frozen=True)
class ProjectId:
    inner: _ProjectId

    @classmethod
    def from_name(cls, name: str) -> ProjectId:
        return ProjectId(_ProjectId(quote(name, safe="")))

    @classmethod
    def from_num(cls, proj_id: int) -> ProjectId:
        return ProjectId(_ProjectId(proj_id))

    @property
    def raw(self) -> str | int:
        if isinstance(self.inner.proj_id, str):
            return unquote(self.inner.proj_id)
        return self.inner.proj_id
