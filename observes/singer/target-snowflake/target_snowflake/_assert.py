# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity import (
    Result,
    ResultE,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


def assert_bool(raw: _T) -> ResultE[bool]:
    if isinstance(raw, bool):
        return Result.success(raw)
    return Result.failure(TypeError("Expected bool"))
