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

_T = TypeVar("_T")


@dataclass(frozen=True)
class Patch(Generic[_T]):
    # patch for https://github.com/python/mypy/issues/5485
    # upgrading mypy where the fix is included will deprecate this
    unwrap: _T
