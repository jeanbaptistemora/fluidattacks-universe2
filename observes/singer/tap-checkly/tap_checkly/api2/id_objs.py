# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from returns.primitives.hkt import (
    SupportsKind2,
)
from typing import (
    TypeVar,
)

_ID = TypeVar("_ID")
_T = TypeVar("_T")


@dataclass(frozen=True)
class IndexedObj(SupportsKind2["IndexedObj[_ID, _T]", _ID, _T]):
    id_obj: _ID
    obj: _T


@dataclass(frozen=True)
class AlertChannelId:
    id_int: int


@dataclass(frozen=True)
class CheckGroupId:
    id_str: str


@dataclass(frozen=True)
class CheckId:
    id_str: str
