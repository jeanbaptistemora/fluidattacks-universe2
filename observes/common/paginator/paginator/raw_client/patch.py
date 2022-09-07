# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from typing import (
    Generic,
    TypeVar,
)

_Point = TypeVar("_Point")


@dataclass(frozen=True)
class Patch(Generic[_Point]):
    # patch for https://github.com/python/mypy/issues/5485
    # upgrading mypy where the fix is included will deprecate this
    inner: _Point

    @property
    def unwrap(self) -> _Point:
        return self.inner
